import asyncio,tempfile,os
from .state import StateStore
from .runtime import JarvisRuntime
from .adapters import WorkerRegistry,Worker,WorkerResult
from .permissions import PermissionEngine

class Fake(Worker):
 name="fake";capabilities={"research","external_send"}
 async def run(self,t):return WorkerResult(True,{"ok":True,"echo":t["step"]["capability"]})

async def main():
 p=os.path.join(tempfile.gettempdir(),"jarvis_next_test.db")
 try:os.remove(p)
 except FileNotFoundError:pass
 r=WorkerRegistry();r.register(Fake())
 x=JarvisRuntime(StateStore(p),r,PermissionEngine("WORK"))
 a=await x.submit("find revenue opportunities")
 assert a["status"]=="awaiting_approval",a
 b=await x.resume(a["approval_id"],approved=True)
 assert b["status"]=="completed",b
 c=await x.submit("research opportunities")
 assert c["status"]=="completed",c
 d=await x.submit("search browser opportunities")
 assert d["status"] in ("completed","failed"),d
 print("JARVIS-NEXT SMOKE OK")

if __name__=="__main__":asyncio.run(main())
