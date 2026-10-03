from dataclasses import dataclass
from enum import Enum
class Profile(str,Enum):
 OBSERVE="OBSERVE"; WORK="WORK"; BUSINESS="BUSINESS"; COMMUNICATION="COMMUNICATION"; EXECUTIVE="EXECUTIVE"; LOCKDOWN="LOCKDOWN"
@dataclass
class Decision:
 allowed:bool; requires_approval:bool; reason:str
class PermissionEngine:
 SAFE={"read","research","analyze","draft","local_file","local_code","test","browser_read"}
 SENSITIVE={"external_send","publish","purchase","payment","delete","legal_commitment","credential_change"}
 def __init__(self,profile="WORK"): self.profile=Profile(profile)
 def check(self,action):
  if self.profile==Profile.LOCKDOWN:return Decision(False,False,"LOCKDOWN profile")
  if action in self.SAFE and self.profile!=Profile.OBSERVE:return Decision(True,False,"permitted safe action")
  if action in self.SENSITIVE:return Decision(False,True,"sensitive action requires approval")
  if self.profile==Profile.OBSERVE:return Decision(False,False,"OBSERVE is read-only")
  return Decision(False,True,"unknown action requires approval")
