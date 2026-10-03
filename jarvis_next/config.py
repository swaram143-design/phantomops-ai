from dataclasses import dataclass
import os
@dataclass
class Settings:
 db_path:str=os.getenv("JARVIS_DB","memory/jarvis_next.db")
 default_permission:str=os.getenv("JARVIS_PERMISSION","WORK")
 model_provider:str=os.getenv("JARVIS_MODEL_PROVIDER","auto")
 model_name:str=os.getenv("JARVIS_MODEL","")
 browser_backend:str=os.getenv("JARVIS_BROWSER_BACKEND","native")
settings=Settings()
