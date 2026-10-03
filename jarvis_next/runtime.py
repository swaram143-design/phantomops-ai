from .state import StateStore
from .permissions import PermissionEngine
from .planner import MissionPlanner
class JarvisRuntime:
 def __init__(self,state=None,workers=None,permissions=None):self.state=state or StateStore();self.workers=workers;self.permissions=permissions or PermissionEngine()
 async def submit(self,goal,context=None):
  mid=self.state.create_mission(goal);plan=MissionPlanner().plan(goal);self.state.update(mid,"planning",plan=plan);results=[];ctx=context or {}
  for step in plan["steps"]:
   d=self.permissions.check(step["action"])
   if d.requires_approval:results.append({"status":"awaiting_approval","approval_id":self.state.approval(mid,step["action"],{**step,**ctx}),"step":step});continue
   ws=self.workers.find(step["capability"]) if self.workers else []
   if not ws:results.append({"status":"blocked","reason":"no worker","step":step});continue
   r=await ws[0].run({"goal":goal,"step":step,**ctx});results.append({"status":"completed" if r.ok else "failed","worker":ws[0].name,"data":r.data,"error":r.error});
   if r.ok and isinstance(r.data,dict):ctx.update(r.data)
  status="awaiting_approval" if any(x["status"]=="awaiting_approval" for x in results) else ("blocked" if any(x["status"]=="blocked" for x in results) else ("failed" if any(x["status"]=="failed" for x in results) else "completed"));self.state.update(mid,status,result=results);return {"mission_id":mid,"status":status,"plan":plan,"results":results}
