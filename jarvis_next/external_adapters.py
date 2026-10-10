import asyncio,os,shutil
from .adapters import Worker,WorkerResult

class BrowserWorker(Worker):
 name="browser";capabilities={"browser_read","research_online"}
 def score(self,task):
  goal=str(task.get("goal","")).lower()
  return 50 if any(x in goal for x in ("browser","website","search","navigate","online")) else 10
 async def run(self,task):
  goal=task.get("goal","")
  try:
   from tools.browser_tools import search_duckduckgo
   result=search_duckduckgo(goal)
   return WorkerResult(True,{"query":goal,"results":result})
  except Exception as e:
   return WorkerResult(False,error=str(e),retryable=True)

class OpenClawAdapter(Worker):
 name="openclaw";capabilities={"computer","channels","persistent_assistant"}
 def score(self,task):
  return 40 if any(x in str(task.get("goal","")).lower() for x in ("computer","desktop","click","type","app")) else 5
 async def run(self,task):
  if not shutil.which("openclaw"): return WorkerResult(False,error="openclaw not installed")
  try:
   p=await asyncio.create_subprocess_exec("openclaw","agent","--message",task.get("goal",""),stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
   out,err=await p.communicate(); stderr=err.decode(errors="replace")[-4000:] if err else None
   if p.returncode!=0: return WorkerResult(False,{"stdout":out.decode(errors="replace")[-12000:]},stderr,retryable=("timeout" in (stderr or "").lower() or "connection" in (stderr or "").lower()))
   return WorkerResult(True,{"stdout":out.decode(errors="replace")[-12000:]})
  except Exception as e: return WorkerResult(False,error=str(e),retryable=True)

class OpenHandsAdapter(Worker):
 name="openhands";capabilities={"code","software_engineering"}
 def score(self,task):
  return 60 if any(x in str(task.get("goal","")).lower() for x in ("code","build","fix","software","github")) else 10

 def _command(self,task):
  goal=str(task.get("goal","")).strip()
  if not goal: raise ValueError("OpenHands requires a non-empty coding goal")
  # OpenHands CLI supports headless scripted execution with --task.
  command=["openhands","--headless","--task",goal]
  if os.getenv("JARVIS_OPENHANDS_JSON","0").lower() in ("1","true","yes"):
   command.insert(2,"--json")
  return command

 async def run(self,task):
  executable=shutil.which("openhands")
  if not executable: return WorkerResult(False,error="openhands not installed")
  try:
   command=self._command(task)
   context=task.get("context") or {}
   cwd=context.get("workspace") or context.get("cwd") or task.get("workspace") or task.get("cwd")
   if cwd:
    cwd=os.path.abspath(os.path.expanduser(str(cwd)))
    if not os.path.isdir(cwd): return WorkerResult(False,error=f"OpenHands workspace does not exist: {cwd}")
   timeout=float(os.getenv("JARVIS_OPENHANDS_TIMEOUT","1800"))
   env=os.environ.copy()
   env.setdefault("PYTHONUNBUFFERED","1")
   p=await asyncio.create_subprocess_exec(*command,executable=executable,cwd=cwd,env=env,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
   try:
    out,err=await asyncio.wait_for(p.communicate(),timeout=timeout)
   except asyncio.TimeoutError:
    p.kill()
    await p.communicate()
    return WorkerResult(False,{"command":command,"cwd":cwd},error=f"OpenHands timed out after {timeout:g}s",retryable=True)
   stdout=out.decode(errors="replace")[-20000:] if out else ""
   stderr=err.decode(errors="replace")[-8000:] if err else ""
   data={"command":command,"cwd":cwd,"returncode":p.returncode,"stdout":stdout,"stderr":stderr}
   if p.returncode!=0:
    transient=any(x in (stdout+" "+stderr).lower() for x in ("timeout","timed out","connection","429","503","502","rate limit","temporarily","try again"))
    return WorkerResult(False,data,error=stderr or f"OpenHands exited with code {p.returncode}",retryable=transient)
   return WorkerResult(True,data)
  except Exception as e:
   return WorkerResult(False,error=str(e),retryable=True)
