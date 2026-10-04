import asyncio,tempfile,os,json
from .state import StateStore
from .runtime import JarvisRuntime
from .adapters import WorkerRegistry,Worker,WorkerResult
from .permissions import PermissionEngine
from .planner import MissionPlanner,PlanValidationError
from .model_router import ModelRouter
from .config import settings

class Fallback(Worker):
    name='fallback'; capabilities={'research'}
    def score(self,task): return 1
    async def run(self,t): return WorkerResult(True,{'fallback':True})

class AlwaysFail(Worker):
    name='always_fail'; capabilities={'research'}
    def score(self,task): return 20
    async def run(self,t): return WorkerResult(False,error='permanent failure')

class Fake(Worker):
    name='fake'; capabilities={'research','external_send'}
    def score(self,task): return 10
    async def run(self,t):
        if t['step']['capability']=='research' and t['attempt']==1 and t['goal']=='retry test': return WorkerResult(False,error='temporary timeout',retryable=True)
        return WorkerResult(True,{'ok':True,'echo':t['step']['capability']})

async def main():
    p=os.path.join(tempfile.gettempdir(),'jarvis_next_test.db')
    try: os.remove(p)
    except FileNotFoundError: pass
    r=WorkerRegistry(); r.register(Fake())
    x=JarvisRuntime(StateStore(p),r,PermissionEngine('WORK'),max_retries=2,retry_delay=0)
    a=await x.submit('find revenue opportunities')
    assert a['status']=='awaiting_approval',a
    assert x.state.conn.execute('SELECT COUNT(*) FROM approvals WHERE mission_id=?',(a['mission_id'],)).fetchone()[0]==1
    resumed=await x.resume_mission(a['mission_id'])
    assert resumed['status']=='awaiting_approval' and resumed['approval_id']==a['approval_id'],resumed
    assert (await x.resume(a['approval_id'],approved=True))['status']=='completed'
    assert (await x.submit('research opportunities'))['status']=='completed'
    r2=WorkerRegistry(); r2.register(AlwaysFail()); r2.register(Fallback())
    fp=os.path.join(tempfile.gettempdir(),'jarvis_next_fallback.db')
    try: os.remove(fp)
    except FileNotFoundError: pass
    x2=JarvisRuntime(StateStore(fp),r2,PermissionEngine('WORK'),max_retries=0,retry_delay=0)
    e=await x2.submit('research opportunities')
    assert e['status']=='completed' and any(item.get('worker')=='fallback' for item in e['results']),e
    d=await x.submit('retry test')
    assert d['status']=='completed',d
    saved=json.loads(x.state.get_mission(d['mission_id'])['result'])
    assert saved['next_step']==1,saved
    try:
        MissionPlanner.validate('bad',{'steps':[{'capability':'shell','action':'execute'}]})
        raise AssertionError('invalid plan accepted')
    except PlanValidationError: pass
    router=ModelRouter(); original=os.environ.pop('OPENAI_API_KEY',None)
    try: assert router.plan('find revenue opportunities',{}) is None
    finally:
        if original is not None: os.environ['OPENAI_API_KEY']=original
    assert settings.max_retries>=0 and settings.retry_delay>=0
    print('JARVIS-NEXT SMOKE OK')

if __name__=='__main__': asyncio.run(main())
