import asyncio,json
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

    async def _run(self,mid,goal,plan,ctx,start_index=0,approval_id=None,approved_step=None,results=None,attempts=None):
        results=list(results or []); attempts=dict(attempts or {}); ctx.setdefault("step_outputs",{})
        for i in range(start_index,len(plan["steps"])):
            step=plan["steps"][i]; decision=self.permissions.check(step["action"])
            if decision.requires_approval and i != approved_step:
                aid=self.state.approval(mid,step["action"],{"step_index":i,"step":step,"context":ctx,"results":results,"attempts":attempts})
                self.state.update(mid,"awaiting_approval",plan=plan,result={"next_step":i,"context":ctx,"results":results,"attempts":attempts})
                return {"mission_id":mid,"status":"awaiting_approval","approval_id":aid,"step":step,"step_index":i,"results":results,"context":ctx}
            if not decision.allowed and i != approved_step:
                item={"status":"blocked","reason":decision.reason,"step":step,"step_index":i}; results.append(item)
                self.state.update(mid,"blocked",plan=plan,result={"next_step":i,"context":ctx,"results":results,"attempts":attempts})
                return {"mission_id":mid,"status":"blocked","results":results,"context":ctx}
            task={"goal":goal,"step":step,"step_index":i,"context":ctx,"mission_id":mid}; task.update(ctx); task["context"]=ctx
            workers=self.workers.ranked(step["capability"],task) if self.workers else []
            if not workers:
                item={"status":"blocked","reason":"no worker","step":step,"step_index":i}; results.append(item)
                self.state.update(mid,"blocked",plan=plan,result={"next_step":i,"context":ctx,"results":results,"attempts":attempts})
                return {"mission_id":mid,"status":"blocked","results":results,"context":ctx}
            step_done=False
            for worker in workers:
                key=f"{i}:{worker.name}"; attempt=attempts.get(key,0)
                while attempt < self.max_retries+1:
                    attempt+=1; attempts[key]=attempt
                    try: result=await worker.run({**task,"attempt":attempt})
                    except Exception as e: result=WorkerResult(False,error=str(e),retryable=self._retryable(e))
                    verified,verification_error=self._verify(step,result)
                    if verified:
                        item={"status":"completed","worker":worker.name,"attempt":attempt,"data":result.data,"error":None,"step":step,"step_index":i}; results.append(item); self._record_output(ctx,i,result.data)
                        self.state.event("step.completed",{"step_index":i,"capability":step["capability"],"worker":worker.name,"attempt":attempt,"verified":True},mid)
                        self.state.update(mid,"running",plan=plan,result={"next_step":i+1,"context":ctx,"results":results,"attempts":attempts}); step_done=True; break
                    error=result.error or verification_error; retryable=result.retryable or self._retryable(error)
                    item={"status":"retrying" if retryable and attempt<=self.max_retries else "failed","worker":worker.name,"attempt":attempt,"data":result.data,"error":error,"step":step,"step_index":i}
                    if retryable and attempt<=self.max_retries:
                        self.state.update(mid,"retrying",plan=plan,result={"next_step":i,"context":ctx,"results":results+[item],"attempts":attempts}); self.state.event("step.retry",{"step_index":i,"worker":worker.name,"attempt":attempt,"error":error},mid); await asyncio.sleep(self.retry_delay*attempt); continue
                    results.append(item); self.state.event("worker.failed",{"step_index":i,"worker":worker.name,"error":error,"fallback_available":len(workers)>1},mid); break
                if step_done: break
                self.state.event("worker.fallback",{"step_index":i,"failed_worker":worker.name},mid)
            if not step_done:
                self.state.update(mid,"failed",plan=plan,result={"next_step":i,"context":ctx,"results":results,"attempts":attempts}); return {"mission_id":mid,"status":"failed","results":results,"context":ctx}
        self.state.update(mid,"completed",plan=plan,result={"next_step":len(plan["steps"]),"context":ctx,"results":results,"attempts":attempts}); return {"mission_id":mid,"status":"completed","results":results,"context":ctx}

    async def submit(self,goal,context=None):
        mid=self.state.create_mission(goal); ctx=dict(context or {}); plan=self.planner.plan(goal,ctx)
        self.state.update(mid,"running",plan=plan,result={"next_step":0,"context":ctx,"results":[],"attempts":{}})
        return await self._run(mid,goal,plan,ctx,0)

    async def resume(self,approval_id,approved=True):
        a=self.state.get_approval(approval_id)
        if not a: raise KeyError(approval_id)
        if a["status"]!="pending": return {"mission_id":a["mission_id"],"status":a["status"],"approval_id":approval_id}
        self.state.resolve_approval(approval_id,"approved" if approved else "rejected")
        mid=a["mission_id"]; m=self.state.get_mission(mid); payload=json.loads(a["payload"]); plan=json.loads(m["plan"])
        if not approved:
            result={"mission_id":mid,"status":"rejected","approval_id":approval_id}; self.state.update(mid,"rejected",plan=plan,result=result); return result
        return await self._run(mid,m["goal"],plan,payload.get("context",{}),payload["step_index"],approval_id,payload["step_index"],payload.get("results",[]),payload.get("attempts",{}))

    async def resume_mission(self,mid):
        m=self.state.get_mission(mid)
        if not m: raise KeyError(mid)
        if m["status"]=="completed": return {"mission_id":mid,"status":"completed"}
        if not m["plan"] or not m["result"]: raise ValueError("Mission has no resumable execution state")
        plan=json.loads(m["plan"]); state=json.loads(m["result"])
        return await self._run(mid,m["goal"],plan,state.get("context",{}),state.get("next_step",0),results=state.get("results",[]),attempts=state.get("attempts",{}))
