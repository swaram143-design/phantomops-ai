import json
import os
import requests

SAFE_ACTIONS={"read","research","analyze","draft","local_file","local_code","test","browser_read","external_send"}
CAPABILITIES={
    "research","opportunity","select_target","proposal","external_send","code","test",
    "browser","research_online","computer","channels","persistent_assistant","software_engineering",
    "legacy_agent","lead","proposal_delivery","email_outreach","followup","analytics",
    "marketplace_mining","marketplace_bidding","live_marketplace","outreach_draft","campaign",
    "inbox_monitor","autonomous_followup","crm_sanitizer","learning_feedback","lead_intelligence",
    "executive_report","govi",
}

class PlanValidationError(ValueError):
    pass

class MissionPlanner:
    def __init__(self, model_router=None):
        self.model_router=model_router

    def deterministic(self,goal):
        g=goal.lower()
        if any(x in g for x in ("revenue","income","client","lead","customer","prospect")):
            steps=[("research","research"),("opportunity","analyze"),("select_target","analyze"),("proposal","draft"),("external_send","external_send")]
        elif any(x in g for x in ("code","build","fix","github","software")):
            steps=[("code","local_code"),("test","test")]
        elif any(x in g for x in ("browser","website","search","find","research online","navigate")):
            steps=[("browser","browser_read")]
        else:
            steps=[("research","research")]
        return {"goal":goal,"steps":[{"capability":c,"action":a} for c,a in steps],"source":"deterministic"}

    @staticmethod
    def validate(goal,plan):
        if not isinstance(plan,dict) or not isinstance(plan.get("steps"),list) or not plan["steps"]:
            raise PlanValidationError("plan must contain a non-empty steps list")
        normalized=[]
        for raw in plan["steps"]:
            if not isinstance(raw,dict):
                raise PlanValidationError("each step must be an object")
            capability=raw.get("capability")
            action=raw.get("action")
            if capability not in CAPABILITIES:
                raise PlanValidationError(f"unknown capability: {capability}")
            if action not in SAFE_ACTIONS:
                raise PlanValidationError(f"unknown or disallowed action: {action}")
            normalized.append({"capability":capability,"action":action})
        return {"goal":goal,"steps":normalized,"source":plan.get("source","model")}

    def _model_plan(self,goal,context=None):
        if not self.model_router:
            return None
        return self.model_router.plan(goal,context or {})

    def plan(self,goal,context=None):
        fallback=self.deterministic(goal)
        try:
            proposed=self._model_plan(goal,context)
            if proposed is not None:
                return self.validate(goal,proposed)
        except Exception:
            pass
        return fallback
