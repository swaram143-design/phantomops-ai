from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List
import json
import os
import logging


# =========================================
# APP
# =========================================

app = FastAPI(
    title="PhantomOps AI API",
    version="1.0.0",
    description="Revenue Automation Infrastructure API"
)


# =========================================
# LOGGING
# =========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("phantomops-api")


# =========================================
# CORS
# =========================================

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# STORAGE
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

LEADS_FILE = os.path.join(
    BASE_DIR,
    "website_leads.json"
)


# =========================================
# MODELS
# =========================================

class Lead(BaseModel):
    name: str
    email: EmailStr
    company: str
    need: str


# =========================================
# HELPERS
# =========================================

def ensure_storage():
    if not os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "w") as file:
            json.dump([], file)


def load_leads() -> List[dict]:

    ensure_storage()

    try:
        with open(LEADS_FILE, "r") as file:
            return json.load(file)

    except Exception as error:

        logger.error(
            f"Failed to load leads: {error}"
        )

        return []


def save_leads(leads: List[dict]):

    try:
        with open(LEADS_FILE, "w") as file:
            json.dump(
                leads,
                file,
                indent=4
            )

    except Exception as error:

        logger.error(
            f"Failed to save leads: {error}"
        )

        raise error


# =========================================
# ROUTES
# =========================================

@app.get("/")
async def home():

    return {
        "status": "online",
        "service": "PhantomOps AI API",
        "version": "1.0.0",
        "runtime": "active"
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "timestamp": str(datetime.utcnow())
    }


@app.get("/leads")
async def get_leads():

    leads = load_leads()

    return {
        "success": True,
        "count": len(leads),
        "leads": leads
    }


@app.post("/submit-lead")
async def submit_lead(lead: Lead):

    leads = load_leads()

    lead_data = {
        "name": lead.name.strip(),
        "email": lead.email.strip(),
        "company": lead.company.strip(),
        "need": lead.need.strip(),
        "created_at": str(datetime.utcnow())
    }

    leads.append(lead_data)

    save_leads(leads)

    logger.info(
        f"NEW LEAD CAPTURED: {lead.email}"
    )

    return {
        "success": True,
        "message": "Lead captured successfully",
        "lead": lead_data
    }


# =========================================
# STARTUP
# =========================================

@app.on_event("startup")
async def startup_event():

    ensure_storage()

    logger.info(
        "PhantomOps AI API Started"
    )


# =========================================
# LOCAL DEV SERVER
# =========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )