import asyncio,tempfile,os,json
from .state import StateStore
from .runtime import JarvisRuntime
from .adapters import WorkerRegistry,Worker,WorkerResult
from .permissions import PermissionEngine
from .planner import MissionPlanner,PlanValidationError

class Fallback(Worker):
    name="fallback"; capabilities={"research"}
    def score(self,task): return 1
    async def run(self,t): return WorkerResult(True,{"fallback":True})

class AlwaysFail(Worker):
    name="always_fail"; capabilities={"research"}
    def score(self,task): return 20
    async def run(self,t): return WorkerResult(False,error="permanent failure")

class Fake(Worker):
    name="fake"; capabilities={"research","external_send"}
    def score(self,task): return 10
    async def run(self,t):
        if t["step"]["capability"]=="research" and t["attempt"]==1 and t["goal"]=="retry test":
            return WorkerResult(False,error="temporary timeout",retryable=True)
        return WorkerResult(True,{"ok":True,"echo":t["step"]["capability"]})

async def main():
    p=os.path.join(tempfile.gettempdir(),"jarvis_next_test.db")
    try: os.remove(p)
    except FileNotFoundError: pass
    r=WorkerRegistry(); r.register(Fake())
    x=JarvisRuntime(StateStore(p),r,PermissionEngine("WORK"),max_retries=2,retry_delay=0)
    a=await x.submit("find revenue opportunities"); assert a["status"]=="awaiting_approval",a
    b=await x.resume(a["approval_id"],approved=True); assert b["status"]=="completed",b
    c=await x.submit("research opportunities"); assert c["status"]=="completed",c
    r2=WorkerRegistry(); r2.register(AlwaysFail()); r2.register(Fallback())
    x2=JarvisRuntime(StateStore(os.path.join(tempfile.gettempdir(),"jarvis_next_fallback.db")),r2,PermissionEngine("WORK"),max_retries=0,retry_delay=0)
    e=await x2.submit("research opportunities"); assert e["status"]=="completed",e
    assert any(item.get("worker")=="fallback" for item in e["results"]),e
    d=await x.submit("retry test"); assert d["status"]=="completed",d
    try:
        MissionPlanner.validate("bad",{"steps":[{"capability":"shell","action":"execute"}]})
        raise AssertionError("invalid plan accepted")
    except PlanValidationError:
        pass
    saved=json.loads(x.state.get_mission(d["mission_id"])["result"]); assert saved["next_step"]==1,saved
    print("JARVIS-NEXT SMOKE OK")

if __name__=="__main__": asyncio.run(main())
