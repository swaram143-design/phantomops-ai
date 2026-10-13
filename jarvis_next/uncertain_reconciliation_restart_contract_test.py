import asyncio,json,tempfile,os
from .adapters import Worker,WorkerRegistry,WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore
from .uncertain_reconciliation import reconcile_uncertain

class AlwaysUncertain(Worker):
    name="uncertain"
    capabilities={"research"}
    def __init__(self): self.calls=0
    async def run(self,task):
        self.calls+=1
        return WorkerResult(False,error="external outcome unknown",retryable=False,side_effect_uncertain=True)

class SuccessWorker(Worker):
    name="success"
    capabilities={"research"}
    def __init__(self): self.calls=0
    async def run(self,task):
        self.calls+=1
        return WorkerResult(True,data={"verified":True})

class FixedPlanner:
    def plan(self,goal,context):
        return {"steps":[{"action":"research","capability":"research","goal":goal}]}

async def run():
    db=tempfile.NamedTemporaryFile(suffix=".db",delete=False); db.close()
    try:
        first_state=StateStore(db.name)
        uncertain=AlwaysUncertain(); workers=WorkerRegistry(); workers.register(uncertain)
        runtime=JarvisRuntime(state=first_state,workers=workers,max_retries=2,retry_delay=0); runtime.planner=FixedPlanner()
        failed=await runtime.submit("restart-safe uncertain mission")
        assert failed["status"]=="failed" and uncertain.calls==1
        mission=first_state.get_mission(failed["mission_id"])
        assert json.loads(mission["result"])["side_effect_uncertain"] is True

        restarted_state=StateStore(db.name)
        success=SuccessWorker(); restarted_workers=WorkerRegistry(); restarted_workers.register(success)
        restarted=JarvisRuntime(state=restarted_state,workers=restarted_workers,max_retries=2,retry_delay=0)
        result=await reconcile_uncertain(restarted,failed["mission_id"],"confirmed_not_applied")
        assert result["status"]=="completed" and success.calls==1
        final=json.loads(restarted_state.get_mission(failed["mission_id"])["result"])
        assert final["reconciliation"]["resolution"]=="confirmed_not_applied"
        assert "side_effect_uncertain" not in final
    finally:
        try: os.remove(db.name)
        except FileNotFoundError: pass

if __name__=="__main__": asyncio.run(run())
