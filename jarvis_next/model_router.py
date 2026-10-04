import json
import os
import requests

class ModelRouter:
    def __init__(self):
        self.providers=[]
        if os.getenv("OPENAI_API_KEY"): self.providers.append("openai")
        if os.getenv("ANTHROPIC_API_KEY"): self.providers.append("anthropic")
        if os.getenv("GOOGLE_API_KEY"): self.providers.append("google")
        if os.getenv("GROQ_API_KEY"): self.providers.append("groq")

    def status(self):
        return {"providers":self.providers,"count":len(self.providers)}

    def choose(self,task_type):
        order={"coding":["openai","anthropic"],"research":["openai","google"],"browser":["openai","google"],"general":["openai","anthropic","google","groq"]}.get(task_type,["openai","anthropic","google","groq"])
        return next((x for x in order if x in self.providers),None)

    def plan(self,goal,context=None):
        provider=self.choose("general")
        if provider!="openai":
            return None
        key=os.getenv("OPENAI_API_KEY")
        if not key:
            return None
        model=os.getenv("JARVIS_MODEL","gpt-6-luna")
        schema={
            "type":"object","additionalProperties":False,
            "properties":{"steps":{"type":"array","items":{"type":"object","additionalProperties":False,"properties":{"capability":{"type":"string"},"action":{"type":"string"}},"required":["capability","action"]}}},
            "required":["steps"]
        }
        prompt=("Create the smallest safe execution plan for this goal. "
                "Use only capabilities and actions supplied by the application contract. "
                "Never invent tools, credentials, URLs, permissions, or actions. "
                f"Goal: {goal}\nContext: {json.dumps(context or {},ensure_ascii=True)}")
        payload={
            "model":model,
            "input":[{"role":"system","content":"You are the JARVIS planning layer. You propose plans only; the application validates and authorizes every step."},{"role":"user","content":prompt}],
            "text":{"format":{"type":"json_schema","name":"jarvis_plan","strict":True,"schema":schema}}
        }
        response=requests.post("https://api.openai.com/v1/responses",headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},json=payload,timeout=30)
        response.raise_for_status()
        data=response.json()
        text=data.get("output_text")
        if not text:
            for item in data.get("output",[]):
                for part in item.get("content",[]):
                    if part.get("type")=="output_text":
                        text=part.get("text"); break
                if text: break
        return json.loads(text) if text else None
