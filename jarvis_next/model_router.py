import json
import os
from urllib import error as urlerror
from urllib import request as urlrequest


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
        if self.choose("general")!="openai" or not os.getenv("OPENAI_API_KEY"):
            return None
        model=os.getenv("JARVIS_MODEL","gpt-6-luna")
        timeout=float(os.getenv("JARVIS_MODEL_TIMEOUT","30"))
        schema={"type":"object","additionalProperties":False,"properties":{"steps":{"type":"array","items":{"type":"object","additionalProperties":False,"properties":{"capability":{"type":"string"},"action":{"type":"string"}},"required":["capability","action"]}}},"required":["steps"]}
        prompt=("Create the smallest safe execution plan for this goal. Use only capabilities and actions supplied by the application contract. Never invent tools, credentials, URLs, permissions, or actions. "
                f"Goal: {goal}\nContext: {json.dumps(context or {},ensure_ascii=True)}")
        payload={"model":model,"input":[{"role":"system","content":"You are the JARVIS planning layer. You propose plans only; the application validates and authorizes every step."},{"role":"user","content":prompt}],"text":{"format":{"type":"json_schema","name":"jarvis_plan","strict":True,"schema":schema}}}
        body=json.dumps(payload).encode("utf-8")
        req=urlrequest.Request(
            "https://api.openai.com/v1/responses",
            data=body,
            headers={"Authorization":f"Bearer {os.getenv('OPENAI_API_KEY')}","Content-Type":"application/json"},
            method="POST",
        )
        try:
            with urlrequest.urlopen(req,timeout=timeout) as response:
                data=json.loads(response.read().decode("utf-8"))
            text=data.get("output_text")
            if not text:
                for item in data.get("output",[]):
                    for part in item.get("content",[]):
                        if part.get("type")=="output_text":
                            text=part.get("text")
                            break
                    if text: break
            return json.loads(text) if text else None
        except (urlerror.URLError,urlerror.HTTPError,TimeoutError,ValueError,TypeError,json.JSONDecodeError):
            return None
