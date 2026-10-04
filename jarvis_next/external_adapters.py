import asyncio,os,shutil
from .adapters import Worker,WorkerResult

class BrowserWorker(Worker):
 name="browser";capabilities={"browser_read","research_online"}
 async def run(self,task):
  goal=task.get("goal","")
  try:
   from tools.browser_tools import search_duckduckgo
   result=search_duckduckgo(goal)
   return WorkerResult(True,{"query":goal,"results":result})
  except Exception as e:
   return WorkerResult(False,error=str(e))

class OpenClawAdapter(Worker):
 name="openclaw";capabilities={"computer","channels","persistent_assistant"}
 async def run(self,task):
  if not shutil.which("openclaw"):return WorkerResult(False,error="openclaw not installed")
  p=await asyncio.create_subprocess_exec("openclaw","agent","--message",task.get("goal",""),stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
  out,err=await p.communicate()
  return WorkerResult(p.returncode==0,{"stdout":out.decode(errors="replace")[-12000:]},err.decode(errors="replace")[-4000:] if err else None)

class OpenHandsAdapter(Worker):
 name="openhands";capabilities={"code","software_engineering"}
 async def run(self,task):
  if not shutil.which("openhands"):return WorkerResult(False,error="openhands not installed")
  p=await asyncio.create_subprocess_exec("openhands","--help",stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
  out,err=await p.communicate()
  return WorkerResult(p.returncode==0,{"stdout":out.decode(errors="replace")[-12000:]},err.decode(errors="replace")[-4000:] if err else None)
