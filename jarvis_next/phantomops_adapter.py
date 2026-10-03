from .adapters import Worker,WorkerResult
class PhantomOpsAdapter(Worker):
 name="phantomops"; capabilities={"research","opportunity","proposal","external_send"}
 async def run(self,task):
  try:
   c=task["step"]["capability"];goal=task["goal"]
   if c=="research":
    from agents.lead_scraper_agent import LeadScraperAgent
    r=await LeadScraperAgent().execute({"description":goal});return WorkerResult(r.get("success",False),r)
   if c=="opportunity":
    from agents.opportunity_agent import OpportunityAgent
    r=await OpportunityAgent().execute({"description":goal});return WorkerResult(r.get("success",False),r)
   if c=="proposal":
    from agents.proposal_agent import ProposalAgent
    r=await ProposalAgent().execute({"company":task.get("company","Prospect"),"need":task.get("need",goal)});return WorkerResult(r.get("success",False),r)
   return WorkerResult(False,error="External send is approval-gated and must be resumed with explicit approval.")
  except Exception as e:return WorkerResult(False,error=str(e))
