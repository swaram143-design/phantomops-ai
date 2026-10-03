import asyncio,os,shutil
from .adapters import Worker,WorkerResult
class CommandWorker(Worker):
 def __init__(self,name,capabilities,command):self.name=name;self.capabilities=set(capabilities);self.command=command
 async def run(self,task):
  if not shutil.which(self.command):return WorkerResult(False,error=f"{self.command} not installed")
  p=await asyncio.create_subprocess_exec(self.command,*self.args(task),stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
  out,err=await p.communicate();return WorkerResult(p.returncode==0,out.decode(errors="replace")[-12000:],err.decode(errors="replace")[-4000:] if err else None)
 def args(self,task):return []
class OpenClawAdapter(CommandWorker):
 def __init__(self):super().__init__("openclaw",{"computer","channels","persistent_assistant"},"openclaw")
 def args(self,task):return ["agent","--message",task["goal"]]
class OpenHandsAdapter(CommandWorker):
 def __init__(self):super().__init__("openhands",{"code","software_engineering"},"openhands")
 def args(self,task):return ["--help"]
