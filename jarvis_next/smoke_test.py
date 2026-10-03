import asyncio,tempfile,os
from .state import StateStore
from .runtime import JarvisRuntime
from .adapters import WorkerRegistry,Worker,WorkerResult
class Fake(Worker):
 name="fake";capabilities={"research"}
 async def run(self,t):return WorkerResult(True,{"ok":True})
async def main():
 p=os.path.join(tempfile.gettempdir(),"jarvis_next_test.db")
 try:os.remove(p)
 except FileNotFoundError:pass
 r=WorkerRegistry();r.register(Fake());x=JarvisRuntime(StateStore(p),r);a=await x.submit("research opportunities");assert a["status"]=="blocked" or a["status"]=="completed";print("JARVIS-NEXT SMOKE OK",a)
if __name__=="__main__":asyncio.run(main())
