from .adapters import Worker,WorkerResult

class PhantomOpsAdapter(Worker):
 name="phantomops";capabilities={"research","opportunity","proposal","external_send"}
 def _pick_target(self,data,goal):
  items=[]
  if isinstance(data,dict):
   for key in ("opportunities","leads"):
    if isinstance(data.get(key),list):items.extend(data[key])
  if not items:return {"company":"Prospect","need":goal,"recipient":None}
  x=items[0] if isinstance(items[0],dict) else {"name":str(items[0])}
  company=x.get("company") or x.get("name") or x.get("title") or "Prospect"
  need=x.get("need") or x.get("description") or x.get("reason") or goal
  recipient=x.get("email") or x.get("recipient") or x.get("contact_email") or x.get("contact")
  return {"company":company,"need":need,"recipient":recipient,"selected_target":x}
 async def run(self,task):
  try:
   c=task["step"]["capability"];goal=task["goal"]
   if c=="research":
    from agents.lead_scraper_agent import LeadScraperAgent
    r=await LeadScraperAgent().execute({"description":goal})
    return WorkerResult(r.get("success",False),r)
   if c=="opportunity":
    from agents.opportunity_agent import OpportunityAgent
    r=await OpportunityAgent().execute({"description":goal,**task})
    return WorkerResult(r.get("success",False),r)
   if c=="proposal":
    target=self._pick_target(task,goal)
    from agents.proposal_agent import ProposalAgent
    r=await ProposalAgent().execute({"company":target["company"],"need":target["need"]})
    if isinstance(r,dict):r.update(target)
    return WorkerResult(r.get("success",False),r)
   if c=="external_send":
    recipient=task.get("recipient")
    if not recipient:
     return WorkerResult(False,error="No verified recipient email is available; refusing to send.")
    from agents.proposal_delivery_agent import ProposalDeliveryAgent
    r=await ProposalDeliveryAgent().execute({"company":task.get("company","Prospect"),"need":task.get("need",goal),"recipient":recipient})
    return WorkerResult(r.get("success",False),r,r.get("error"))
   return WorkerResult(False,error=f"Unsupported capability: {c}")
  except Exception as e:return WorkerResult(False,error=str(e))
