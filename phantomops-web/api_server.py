from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

import json
import os


app = FastAPI()


# =========================
# CORS
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================
# MODEL
# =========================

class Lead(BaseModel):

    name: str

    email: str

    company: str

    need: str


# =========================
# STORAGE
# =========================

LEADS_FILE = (
    "website_leads.json"
)


def load_leads():

    if not os.path.exists(
        LEADS_FILE
    ):
        return []

    with open(
        LEADS_FILE,
        "r"
    ) as file:

        return json.load(
            file
        )


def save_leads(
    leads
):

    with open(
        LEADS_FILE,
        "w"
    ) as file:

        json.dump(
            leads,
            file,
            indent=4
        )


# =========================
# ROUTES
# =========================

@app.get("/")
async def home():

    return {

        "status":
            "PhantomOps API Running"
    }


@app.post("/submit-lead")
async def submit
    lead: Lead
):

    leads = load_leads()

    lead_data = {

        "name":
            lead.name,

        "email":
            lead.email,

        "company":
            lead.company,

        "need":
            lead.need,

        "created_at":
            str(
                datetime.now()
            )
    }

    leads.append(
        lead_data
    )

    save_leads(
        leads
    )

    print(
        "\n[NEW LEAD]",
        lead_data,
        "\n"
    )

    return {

        "success": True,

        "message":
            "Lead captured successfully",

        "lead":
            lead_data
    }