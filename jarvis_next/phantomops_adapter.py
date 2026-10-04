from .adapters import Worker,WorkerResult

class PhantomOpsAdapter(Worker):
 name="phantomops";capabilities={"research","opportunity","proposal","external_send"}
 def _pick_target(self,data,goal):
  items=[]
  if isinstance(data,dict):
   for key in ("opportunities","leads"):
    if isinstance(data.get(key),list): items.extend(data[key])
  if not items:return {"company":"Prospect","need":goal}
  x=items[0] if isinstance(items[0],dict) else {"name":str(items[0])}
  company=x.get("company") or x.get("name") or x.get("title") or "Prospect"
  need=x.get("need") or x.get("description") or x.get("reason") or goal
  return {"company":company,"need":need,"selected_target":x}
 async def run(self,task):
  try:
   c=task["step"]["capability"];goal=task["goal"]
   if c=="research":
    from agents.lead_scraper_agent import LeadScraperAgent
    r=await LeadScraperAgent().execute({"description":goal});return WorkerResult(r.get("success",False),r)
   if c=="opportunity":
    from agents.opportunity_agent import OpportunityAgent
    r=await OpportunityAgent().execute({"description":goal,**task});return WorkerResult(r.get("success",False),r)
   if c=="proposal":
    target=self._pick_target(task,goal)
    from agents.proposal_agent import ProposalAgent
    r=await ProposalAgent().execute({"company":target["company"],"need":target["need"]})
    if isinstance(r,dict):r.update(target)
    return WorkerResult(r.get("success",False),r)
   return WorkerResult(False,error="External send is approval-gated; use the runtime resume() path after explicit approval.")
  except Exception as e:return WorkerResult(False,error=str(e))
