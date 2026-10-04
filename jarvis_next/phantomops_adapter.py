from .adapters import Worker,WorkerResult

class PhantomOpsAdapter(Worker):
 name="phantomops";capabilities={"research","opportunity","select_target","proposal","external_send"}
 def score(self,task):
  goal=str(task.get("goal","")).lower()
  step=task.get("step",{})
  cap=step.get("capability","")
  score=20
  if cap in self.capabilities: score+=20
  if any(x in goal for x in ("revenue","lead","client","customer","prospect","proposal","automation")): score+=30
  return score
 def _context(self,task):
  context=task.get("context")
  return context if isinstance(context,dict) else {}
 def _items(self,data):
  if not isinstance(data,dict):return []
  items=[]
  for key in ("opportunities","leads"):
   if isinstance(data.get(key),list):items.extend(x for x in data[key] if isinstance(x,dict))
  return items
 def _pick_target(self,data,goal):
  items=self._items(data)
  if not items:return {"company":"Prospect","need":goal,"recipient":None,"selected_target":None}
  def score(x):
   s=0
   for k in ("email","contact_email","recipient"): s+=3 if x.get(k) else 0
   for k in ("website","company","name","title"): s+=1 if x.get(k) else 0
   for k in ("intent","score","opportunity_score","buyer_intent"):
    v=x.get(k)
    if isinstance(v,(int,float)):s+=min(float(v),10)
   return s
  x=max(items,key=score)
  company=x.get("company") or x.get("name") or x.get("title") or "Prospect"
  need=x.get("need") or x.get("description") or x.get("reason") or goal
  recipient=x.get("email") or x.get("recipient") or x.get("contact_email") or x.get("contact")
  return {"company":company,"need":need,"recipient":recipient,"selected_target":x,"selection_score":score(x)}
 async def run(self,task):
  try:
   c=task["step"]["capability"];goal=task["goal"];ctx=self._context(task)
   merged={**ctx,**task}
   if c=="research":
    from agents.lead_scraper_agent import LeadScraperAgent
    r=await LeadScraperAgent().execute({"description":goal,**ctx})
    return WorkerResult(r.get("success",False),r,r.get("error"))
   if c=="opportunity":
    from agents.opportunity_agent import OpportunityAgent
    r=await OpportunityAgent().execute({"description":goal,**ctx,**task})
    return WorkerResult(r.get("success",False),r,r.get("error"))
   if c=="select_target":
    target=self._pick_target(merged,goal)
    return WorkerResult(True,target)
   if c=="proposal":
    target=merged if merged.get("selected_target") else self._pick_target(merged,goal)
    payload={"company":target.get("company","Prospect"),"need":target.get("need",goal)}
    from agents.proposal_agent import ProposalAgent
    r=await ProposalAgent().execute(payload)
    if isinstance(r,dict):r.update(target)
    return WorkerResult(r.get("success",False),r,r.get("error"))
   if c=="external_send":
    recipient=merged.get("recipient")
    if not recipient:
     return WorkerResult(False,error="No verified recipient email is available; refusing to send.")
    from agents.proposal_delivery_agent import ProposalDeliveryAgent
    r=await ProposalDeliveryAgent().execute({
      "company":merged.get("company","Prospect"),
      "need":merged.get("need",goal),
      "recipient":recipient,
      **({"proposal":merged["proposal"]} if "proposal" in merged else {}),
    })
    return WorkerResult(r.get("success",False),r,r.get("error"))
   return WorkerResult(False,error=f"Unsupported capability: {c}")
  except Exception as e:
   return WorkerResult(False,error=str(e))
