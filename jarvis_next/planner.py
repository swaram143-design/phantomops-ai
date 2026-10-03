class MissionPlanner:
 def plan(self,goal):
  g=goal.lower()
  if any(x in g for x in ("revenue","income","client","lead","customer")):steps=[("research","research"),("opportunity","analyze"),("proposal","draft"),("external_send","external_send")]
  elif any(x in g for x in ("code","build","fix","github","software")):steps=[("code","local_code"),("test","test")]
  elif any(x in g for x in ("browser","website","search","find")):steps=[("browser","browser_read")]
  else:steps=[("research","research")]
  return {"goal":goal,"steps":[{"capability":c,"action":a} for c,a in steps]}
