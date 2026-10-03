import os
class ModelRouter:
 def __init__(self):
  self.providers=[]
  if os.getenv("OPENAI_API_KEY"):self.providers.append("openai")
  if os.getenv("ANTHROPIC_API_KEY"):self.providers.append("anthropic")
  if os.getenv("GOOGLE_API_KEY"):self.providers.append("google")
  if os.getenv("GROQ_API_KEY"):self.providers.append("groq")
 def status(self):return {"providers":self.providers,"count":len(self.providers)}
 def choose(self,task_type):
  order={"coding":["openai","anthropic"],"research":["openai","google"],"browser":["openai","google"],"general":["openai","anthropic","google","groq"]}.get(task_type,["openai","anthropic","google","groq"])
  return next((x for x in order if x in self.providers),None)
