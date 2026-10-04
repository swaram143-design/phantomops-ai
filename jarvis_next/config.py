from dataclasses import dataclass
import os

@dataclass
class Settings:
    db_path:str=os.getenv("JARVIS_DB","memory/jarvis_next.db")
    default_permission:str=os.getenv("JARVIS_PERMISSION","WORK")
    model_provider:str=os.getenv("JARVIS_MODEL_PROVIDER","auto")
    model_name:str=os.getenv("JARVIS_MODEL","")
    model_timeout:float=float(os.getenv("JARVIS_MODEL_TIMEOUT","30"))
    browser_backend:str=os.getenv("JARVIS_BROWSER_BACKEND","native")
    max_retries:int=int(os.getenv("JARVIS_MAX_RETRIES","2"))
    retry_delay:float=float(os.getenv("JARVIS_RETRY_DELAY","1"))
    nexus_root:str=os.getenv("NEXUS_ROOT","")

settings=Settings()
