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
    @staticmethod
    def _durable(value):
        return json.loads(json.dumps(value,default=str))
    def _verify(self,step,result):
        if not result.ok: return False,result.error or "worker reported failure"
        return self.verifier.verify(step,result.data)
    @staticmethod
    def _record_output(ctx,index,data):
        ctx.setdefault("step_outputs",{})[str(index)]=data
        if not isinstance(data,dict): return
        protected={"goal","step","step_index","context","mission_id","attempt","idempotency_key","company","recipient","selected_target","selection_score"}
        for key,value in data.items():
            if key not in protected or key not in ctx: ctx[key]=value
    @staticmethod
    def _result_state(next_step,ctx,results,attempts,reconciliation=None,**extra):
        payload={"next_step":next_step,"context":ctx,"results":results,"attempts":attempts}
        if reconciliation is not None: payload["reconciliation"]=reconciliation
        payload.update(extra)
        return payload
    def _update(self,mid,owner,**kwargs): self.state.update(mid,lease_owner=owner,**kwargs)
    async def _lease_heartbeat(self,mid,owner,stop):
        interval=max(0.1,float(settings.mission_lease_seconds)/3.0)
        while not stop.is_set():
            try: await asyncio.wait_for(stop.wait(),timeout=interval)
            except asyncio.TimeoutError:
                if not self.state.renew_mission(mid,owner): return False
        return True
    async def _run(self,mid,goal,plan,ctx,start_index=0,approval_id=None,approved_step=None,results=None,attempts=None,lease_owner=None,reconciliation=None):
        results=list(results or []); attempts=dict(attempts or {}); ctx=self._durable(ctx); ctx.setdefault("step_outputs",{})
        for i in range(start_index,len(plan["steps"])):
            if lease_owner is not None and not self.state.has_mission_lease(mid,lease_owner):
                return {"mission_id":mid,"status":"lease_lost","error":"mission lease lost","results":results,"context":ctx}
            step=plan["steps"][i]; decision=self.permissions.check(step["action"])
            if decision.requires_approval and i != approved_step:
                aid=self.state.approval(mid,step["action"],{"step_index":i,"step":step,"context":ctx,"results":results,"attempts":attempts})
                self._update(mid,lease_owner,status="awaiting_approval",plan=plan,result=self._result_state(i,ctx,results,attempts,reconciliation))
                return {"mission_id":mid,"status":"awaiting_approval","approval_id":aid,"step":step,"step_index":i,"results":results,"context":ctx}
            if not decision.allowed and i != approved_step:
                item={"status":"blocked","reason":decision.reason,"step":step,"step_index":i}; results.append(item)
                self._update(mid,lease_owner,status="blocked",plan=plan,result=self._result_state(i,ctx,results,attempts,reconciliation))
                return {"mission_id":mid,"status":"blocked","results":results,"context":ctx}
            task=dict(ctx)
            task.update({"goal":goal,"step":step,"step_index":i,"context":ctx,"mission_id":mid})
            workers=self.workers.ranked(step["capability"],task) if self.workers else []
            if not workers:
                item={"status":"blocked","reason":"no worker","step":step,"step_index":i}; results.append(item)
                self._update(mid,lease_owner,status="blocked",plan=plan,result=self._result_state(i,ctx,results,attempts,reconciliation))
                return {"mission_id":mid,"status":"blocked","results":results,"context":ctx}
            step_done=False; uncertain_outcome=False
            for worker in workers:
                if lease_owner is not None and not self.state.has_mission_lease(mid,lease_owner):
                    return {"mission_id":mid,"status":"lease_lost","error":"mission lease lost","results":results,"context":ctx}
                key=f"{i}:{worker.name}"; attempt=attempts.get(key,0); execution_key=f"{mid}:{i}:{worker.name}"
                while attempt < self.max_retries+1:
                    if lease_owner is not None and not self.state.has_mission_lease(mid,lease_owner):
                        return {"mission_id":mid,"status":"lease_lost","error":"mission lease lost","results":results,"context":ctx}
                    attempt+=1; attempts[key]=attempt
                    try: result=await worker.run({**task,"attempt":attempt,"idempotency_key":execution_key})
                    except Exception as e: result=WorkerResult(False,error=str(e),retryable=self._retryable(e))
                    if result.ok: result=WorkerResult(True,data=self._durable(result.data),error=result.error,retryable=result.retryable,side_effect_uncertain=result.side_effect_uncertain)
                    # An uncertain external outcome always takes precedence over
                    # an otherwise successful transport response. We cannot safely
                    # mark the step completed until the external state is reconciled.
                    if result.side_effect_uncertain:
                        item={"status":"failed","worker":worker.name,"attempt":attempt,"data":result.data,"error":result.error or "external outcome unknown","step":step,"step_index":i,"side_effect_uncertain":True}
                        results.append(item)
                        self.state.event("worker.uncertain",{"step_index":i,"worker":worker.name,"attempt":attempt,"error":item["error"],"fallback_blocked":True},mid)
                        uncertain_outcome=True
                        break
                    verified,verification_error=self._verify(step,result)
                    if verified:
                        item={"status":"completed","worker":worker.name,"attempt":attempt,"data":result.data,"error":None,"step":step,"step_index":i}; results.append(item); self._record_output(ctx,i,result.data)
                        self.state.update_with_event(mid,lease_owner=lease_owner,status="running",plan=plan,result=self._result_state(i+1,ctx,results,attempts,reconciliation),event_kind="step.completed",event_payload={"step_index":i,"capability":step["capability"],"worker":worker.name,"attempt":attempt,"verified":True})
                        step_done=True; break
                    error=result.error or verification_error; retryable=result.retryable if result.error is not None else self._retryable(error)
                    item={"status":"retrying" if retryable and attempt<=self.max_retries else "failed","worker":worker.name,"attempt":attempt,"data":result.data,"error":error,"step":step,"step_index":i}
                    if retryable and attempt<=self.max_retries:
                        self.state.update_with_event(mid,lease_owner=lease_owner,status="retrying",plan=plan,result=self._result_state(i,ctx,results+[item],attempts,reconciliation),event_kind="step.retry",event_payload={"step_index":i,"worker":worker.name,"attempt":attempt,"error":error})
                        await asyncio.sleep(self.retry_delay*attempt); continue
                    results.append(item); self.state.event("worker.failed",{"step_index":i,"worker":worker.name,"error":error,"fallback_available":len(workers)>1},mid); break
                if step_done or uncertain_outcome: break
                if lease_owner is not None and not self.state.has_mission_lease(mid,lease_owner):
                    return {"mission_id":mid,"status":"lease_lost","error":"mission lease lost","results":results,"context":ctx}
                self.state.event("worker.fallback",{"step_index":i,"failed_worker":worker.name},mid)
            if not step_done:
                result_payload=self._result_state(i,ctx,results,attempts,reconciliation,side_effect_uncertain=uncertain_outcome) if uncertain_outcome else self._result_state(i,ctx,results,attempts,reconciliation)
                self._update(mid,lease_owner,status="failed",plan=plan,result=result_payload); return {"mission_id":mid,"status":"failed","results":results,"context":ctx,"side_effect_uncertain":uncertain_outcome,"reconciliation":reconciliation}
        self._update(mid,lease_owner,status="completed",plan=plan,result=self._result_state(len(plan["steps"]),ctx,results,attempts,reconciliation)); return {"mission_id":mid,"status":"completed","results":results,"context":ctx,"reconciliation":reconciliation}
    async def _run_owned(self,mid,goal,plan,ctx,owner,**kwargs):
        stop=asyncio.Event(); heartbeat=asyncio.create_task(self._lease_heartbeat(mid,owner,stop))
        try:
            try: return await self._run(mid,goal,plan,ctx,lease_owner=owner,**kwargs)
            except RuntimeError as e:
                if str(e) != "mission lease lost": raise
                return {"mission_id":mid,"status":"lease_lost","error":"mission lease lost"}
        finally: stop.set(); await heartbeat
    async def submit(self,goal,context=None):
        mid=self.state.create_mission(goal); ctx=self._durable(dict(context or {}))
        try: plan=self.planner.plan(goal,ctx)
        except Exception as e:
            error=str(e) or e.__class__.__name__; result={"mission_id":mid,"status":"failed","error":error}; self.state.update_with_event(mid,status="failed",result=result,event_kind="mission.planning_failed",event_payload={"error":error}); return result
        self.state.update(mid,"running",plan=plan,result={"next_step":0,"context":ctx,"results":[],"attempts":{}})
        owner=str(uuid.uuid4())
        if not self.state.claim_mission(mid,owner,statuses=("running",)): raise RuntimeError("failed to claim newly created mission")
        try: return await self._run_owned(mid,goal,plan,ctx,owner,start_index=0)
        finally: self.state.release_mission(mid,owner)
    async def resume(self,approval_id,approved=True):
        a=self.state.get_approval(approval_id)
        if not a: raise KeyError(approval_id)
        if a["status"]!="pending": return {"mission_id":a["mission_id"],"status":a["status"],"approval_id":approval_id}
        mid=a["mission_id"]; owner=str(uuid.uuid4())
        if not self.state.claim_mission(mid,owner,statuses=("awaiting_approval","running","retrying","blocked")):
            current=self.state.get_mission(mid); return {"mission_id":mid,"status":"already_running","approval_id":approval_id,"current_status":current["status"] if current else None}
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
            payload=json.loads(pending["payload"]); return {"mission_id":mid,"status":"awaiting_approval","approval_id":pending["id"],"step":payload.get("step"),"step_index":payload.get("step_index"),"results":payload.get("results",[]),"context":payload.get("context",{})}
        if not m["plan"] or not m["result"]: raise ValueError("Mission has no resumable execution state")
        owner=str(uuid.uuid4())
        if not self.state.claim_mission(mid,owner):
            current=self.state.get_mission(mid); return {"mission_id":mid,"status":"already_running","current_status":current["status"] if current else None}
        try:
            m=self.state.get_mission(mid); plan=json.loads(m["plan"]); state=json.loads(m["result"])
            return await self._run_owned(mid,m["goal"],plan,state.get("context",{}),owner,start_index=state.get("next_step",0),results=state.get("results",[]),attempts=state.get("attempts",{}),reconciliation=state.get("reconciliation"))
        finally: self.state.release_mission(mid,owner)