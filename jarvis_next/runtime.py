import asyncio,json,uuid
from .state import StateStore
from .permissions import PermissionEngine
from .planner import MissionPlanner
from .model_router import ModelRouter
from .verifier import ResultVerifier
from .adapters import WorkerResult
from .config import settings

class JarvisRuntime:
    def __init__(self,state=None,workers=None,permissions=None,max_retries=None,retry_delay=None):
        self.state=state or StateStore(); self.workers=workers
        self.permissions=permissions or PermissionEngine(settings.default_permission)
        self.planner=MissionPlanner(ModelRouter()); self.verifier=ResultVerifier()
        self.max_retries=int(settings.max_retries if max_retries is None else max_retries)
        self.retry_delay=float(settings.retry_delay if retry_delay is None else retry_delay)

    @staticmethod
    def _retryable(error):
        if not error: return False
        e=str(error).lower()
        return any(x in e for x in ("timeout","timed out","temporarily","connection","429","503","502","rate limit","busy","try again","network"))

    def _verify(self,step,result):
        if not result.ok: return False,result.error or "worker reported failure"
        return self.verifier.verify(step,result.data)

    @staticmethod
    def _record_output(ctx,index,data):
        ctx.setdefault("step_outputs",{})[str(index)]=data
        if not isinstance(data,dict): return
        protected={"company","recipient","selected_target","selection_score"}
        for key,value in data.items():
            if key not in protected or key not in ctx: ctx[key]=value

    def _update(self,mid,owner,**kwargs):
        self.state.update(mid,lease_owner=owner,**kwargs)

    async def _lease_heartbeat(self,mid,owner,stop):
        interval=max(0.1,float(settings.mission_lease_seconds)/3.0)
        while not stop.is_set():
            try:
                await asyncio.wait_for(stop.wait(),timeout=interval)
            except asyncio.TimeoutError:
                if not self.state.renew_mission(mid,owner): return False
        return True

    async def _run(self,mid,goal,plan,ctx,start_index=0,approval_id=None,approved_step=None,results=None,attempts=None,lease_owner=None):
        results=list(results or []); attempts=dict(attempts or {}); ctx.setdefault("step_outputs",{})
        for i in range(start_index,len(plan["steps"])):
            step=plan["steps"][i]; decision=self.permissions.check(step["action"])
            if decision.requires_approval and i != approved_step:
                aid=self.state.approval(mid,step["action"],{"step_index":i,"step":step,"context":ctx,"results":results,"attempts":attempts})
                self._update(mid,lease_owner,status="awaiting_approval",plan=plan,result={"next_step":i,"context":ctx,"results":results,"attempts":attempts})
                return {"mission_id":mid,"status":"awaiting_approval","approval_id":aid,"step":step,"step_index":i,"results":results,"context":ctx}
            if not decision.allowed and i != approved_step:
                item={"status":"blocked","reason":decision.reason,"step":step,"step_index":i}; results.append(item)
                self._update(mid,lease_owner,status="blocked",plan=plan,result={"next_step":i,"context":ctx,"results":results,"attempts":attempts})
                return {"mission_id":mid,"status":"blocked","results":results,"context":ctx}
            task={"goal":goal,"step":step,"step_index":i,"context":ctx,"mission_id":mid}; task.update(ctx); task["context"]=ctx
            workers=self.workers.ranked(step["capability"],task) if self.workers else []
            if not workers:
                item={"status":"blocked","reason":"no worker","step":step,"step_index":i}; results.append(item)
                self._update(mid,lease_owner,status="blocked",plan=plan,result={"next_step":i,"context":ctx,"results":results,"attempts":attempts})
                return {"mission_id":mid,"status":"blocked","results":results,"context":ctx}
            step_done=False
            for worker in workers:
                key=f"{i}:{worker.name}"; attempt=attempts.get(key,0)
                execution_key=f"{mid}:{i}:{worker.name}"
                while attempt < self.max_retries+1:
                    attempt+=1; attempts[key]=attempt
                    try: result=await worker.run({**task,"attempt":attempt,"idempotency_key":execution_key})
                    except Exception as e: result=WorkerResult(False,error=str(e),retryable=self._retryable(e))
                    verified,verification_error=self._verify(step,result)
                    if verified:
                        item={"status":"completed","worker":worker.name,"attempt":attempt,"data":result.data,"error":None,"step":step,"step_index":i}; results.append(item); self._record_output(ctx,i,result.data)
                        self.state.event("step.completed",{"step_index":i,"capability":step["capability"],"worker":worker.name,"attempt":attempt,"verified":True},mid)
                        self._update(mid,lease_owner,status="running",plan=plan,result={"next_step":i+1,"context":ctx,"results":results,"attempts":attempts}); step_done=True; break
                    error=result.error or verification_error; retryable=result.retryable or self._retryable(error)
                    item={"status":"retrying" if retryable and attempt<=self.max_retries else "failed","worker":worker.name,"attempt":attempt,"data":result.data,"error":error,"step":step,"step_index":i}
                    if retryable and attempt<=self.max_retries:
                        self._update(mid,lease_owner,status="retrying",plan=plan,result={"next_step":i,"context":ctx,"results":results+[item],"attempts":attempts}); self.state.event("step.retry",{"step_index":i,"worker":worker.name,"attempt":attempt,"error":error},mid); await asyncio.sleep(self.retry_delay*attempt); continue
                    results.append(item); self.state.event("worker.failed",{"step_index":i,"worker":worker.name,"error":error,"fallback_available":len(workers)>1},mid); break
                if step_done: break
                self.state.event("worker.fallback",{"step_index":i,"failed_worker":worker.name},mid)
            if not step_done:
                self._update(mid,lease_owner,status="failed",plan=plan,result={"next_step":i,"context":ctx,"results":results,"attempts":attempts}); return {"mission_id":mid,"status":"failed","results":results,"context":ctx}
        self._update(mid,lease_owner,status="completed",plan=plan,result={"next_step":len(plan["steps"]),"context":ctx,"results":results,"attempts":attempts}); return {"mission_id":mid,"status":"completed","results":results,"context":ctx}

    async def _run_owned(self,mid,goal,plan,ctx,owner,**kwargs):
        stop=asyncio.Event(); heartbeat=asyncio.create_task(self._lease_heartbeat(mid,owner,stop))
        try:
            try: return await self._run(mid,goal,plan,ctx,lease_owner=owner,**kwargs)
            except RuntimeError as e:
                if str(e) != "mission lease lost": raise
                return {"mission_id":mid,"status":"lease_lost","error":"mission lease lost"}
        finally:
            stop.set(); await heartbeat

    async def submit(self,goal,context=None):
        mid=self.state.create_mission(goal); ctx=dict(context or {})
        try: plan=self.planner.plan(goal,ctx)
        except Exception as e:
            error=str(e) or e.__class__.__name__; result={"mission_id":mid,"status":"failed","error":error}
            self.state.update(mid,"failed",result=result); self.state.event("mission.planning_failed",{"error":error},mid); return result
        self.state.update(mid,"running",plan=plan,result={"next_step":0,"context":ctx,"results":[],"attempts":{}})
        owner=str(uuid.uuid4())
        if not self.state.claim_mission(mid,owner,statuses=("running",)): raise RuntimeError("failed to claim newly created mission")
        try: return await self._run_owned(mid,goal,plan,ctx,owner,start_index=0)
        finally: self.state.release_mission(mid,owner)

    async def resume(self,approval_id,approved=True):
        a=self.state.get_approval(approval_id)
        if not a: raise KeyError(approval_id)
        if a["status"]!="pending": return {"mission_id":a["mission_id"],"status":a["status"],"approval_id":approval_id}
        mid=a["mission_id"]
        owner=str(uuid.uuid4())
        if not self.state.claim_mission(mid,owner,statuses=("awaiting_approval","running","retrying","blocked")):
            current=self.state.get_mission(mid)
            return {"mission_id":mid,"status":"already_running","approval_id":approval_id,"current_status":current["status"] if current else None}
        try:
            resolved=self.state.resolve_approval(approval_id,"approved" if approved else "rejected")
            if resolved is None:
                current=self.state.get_approval(approval_id); return {"mission_id":mid,"status":current["status"],"approval_id":approval_id}
            m=self.state.get_mission(mid); payload=json.loads(a["payload"]); plan=json.loads(m["plan"])
            if not approved:
                result={"mission_id":mid,"status":"rejected","approval_id":approval_id}; self._update(mid,owner,status="rejected",plan=plan,result=result); return result
            return await self._run_owned(mid,m["goal"],plan,payload.get("context",{}),owner,start_index=payload.get("step_index",0),approval_id=approval_id,approved_step=payload.get("step_index"),results=payload.get("results",[]),attempts=payload.get("attempts",{}))
        finally: self.state.release_mission(mid,owner)

    async def resume_mission(self,mid):
        m=self.state.get_mission(mid)
        if not m: raise KeyError(mid)
        if m["status"] in ("completed","failed","rejected"): return {"mission_id":mid,"status":m["status"]}
        if m["status"]=="awaiting_approval":
            pending=self.state.pending_approval(mid)
            if not pending: return {"mission_id":mid,"status":"awaiting_approval","approval_id":None}
            payload=json.loads(pending["payload"])
            return {"mission_id":mid,"status":"awaiting_approval","approval_id":pending["id"],"step":payload.get("step"),"step_index":payload.get("step_index"),"results":payload.get("results",[]),"context":payload.get("context",{})}
        if not m["plan"] or not m["result"]: raise ValueError("Mission has no resumable execution state")
        owner=str(uuid.uuid4())
        if not self.state.claim_mission(mid,owner):
            current=self.state.get_mission(mid); return {"mission_id":mid,"status":"already_running","current_status":current["status"] if current else None}
        try:
            m=self.state.get_mission(mid); plan=json.loads(m["plan"]); state=json.loads(m["result"])
            return await self._run_owned(mid,m["goal"],plan,state.get("context",{}),owner,start_index=state.get("next_step",0),results=state.get("results",[]),attempts=state.get("attempts",{}))
        finally: self.state.release_mission(mid,owner)
