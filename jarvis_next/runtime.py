import json
from .state import StateStore
from .permissions import PermissionEngine
from .planner import MissionPlanner

class JarvisRuntime:
 def __init__(self,state=None,workers=None,permissions=None):
  self.state=state or StateStore();self.workers=workers;self.permissions=permissions or PermissionEngine()
 async def _run(self,mid,goal,plan,ctx,start_index=0,approval_id=None,approved_step=None):
  results=[]
  for i,step in enumerate(plan["steps"][start_index:],start=start_index):
   d=self.permissions.check(step["action"])
   if d.requires_approval and i != approved_step:
    aid=approval_id or self.state.approval(mid,step["action"],{"step_index":i,"step":step,"context":ctx})
    self.state.update(mid,"awaiting_approval",plan=plan,result=results)
    return {"mission_id":mid,"status":"awaiting_approval","approval_id":aid,"step":step,"step_index":i,"results":results}
   if not d.allowed and i != approved_step:
    results.append({"status":"blocked","reason":d.reason,"step":step,"step_index":i})
    continue
   ws=self.workers.find(step["capability"]) if self.workers else []
   if not ws:
    results.append({"status":"blocked","reason":"no worker","step":step,"step_index":i})
    continue
   r=await ws[0].run({"goal":goal,"step":step,**ctx})
   item={"status":"completed" if r.ok else "failed","worker":ws[0].name,"data":r.data,"error":r.error,"step":step,"step_index":i}
   results.append(item)
   if not r.ok:
    self.state.update(mid,"failed",plan=plan,result=results)
    return {"mission_id":mid,"status":"failed","results":results}
   if isinstance(r.data,dict):ctx.update(r.data)
   self.state.event("step.completed",{"step_index":i,"capability":step["capability"],"ok":r.ok},mid)
  status="completed" if not any(x["status"] in ("blocked","failed") for x in results) else "blocked"
  self.state.update(mid,status,plan=plan,result={"results":results,"context":ctx})
  return {"mission_id":mid,"status":status,"results":results,"context":ctx}
 async def submit(self,goal,context=None):
  mid=self.state.create_mission(goal);plan=MissionPlanner().plan(goal);self.state.update(mid,"running",plan=plan)
  return await self._run(mid,goal,plan,context or {},0)
 async def resume(self,approval_id,approved=True):
  a=self.state.get_approval(approval_id)
  if not a: raise KeyError(approval_id)
  if a["status"]!="pending": return {"mission_id":a["mission_id"],"status":a["status"],"approval_id":approval_id}
  self.state.resolve_approval(approval_id,"approved" if approved else "rejected")
  mid=a["mission_id"];m=self.state.get_mission(mid)
  payload=json.loads(a["payload"]);plan=json.loads(m["plan"]);ctx=payload.get("context",{})
  if not approved:
   result={"mission_id":mid,"status":"rejected","approval_id":approval_id}
   self.state.update(mid,"rejected",plan=plan,result=result);return result
  return await self._run(mid,m["goal"],plan,ctx,payload["step_index"],approval_id,approved_step=payload["step_index"])
