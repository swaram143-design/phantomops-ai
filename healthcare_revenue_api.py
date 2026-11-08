"""Single-tenant healthcare enquiry operations API for paid pilot deployments.

This MVP stores only basic enquiry/contact workflow data. Do not store diagnoses,
clinical notes, prescriptions, reports, or other medical-record content here.
Deploy one isolated instance per customer until tenant isolation and a full
security review are implemented.
"""
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="PhantomOps Healthcare Revenue Desk",
    version="0.1.0",
    description="Single-customer pilot API for enquiry tracking and follow-up operations.",
)

DB_PATH = os.getenv("PHANTOMOPS_HEALTHCARE_DB", "data/healthcare_revenue.db")
ALLOWED_STATUSES = {"new", "contacted", "appointment_booked", "completed", "closed"}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def connect():
    parent = os.path.dirname(DB_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS enquiries (
                id TEXT PRIMARY KEY,
                contact_name TEXT NOT NULL,
                contact_phone TEXT NOT NULL,
                service_category TEXT NOT NULL,
                source TEXT NOT NULL,
                status TEXT NOT NULL,
                next_followup_at TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        db.execute("CREATE INDEX IF NOT EXISTS idx_enquiries_status ON enquiries(status)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_enquiries_followup ON enquiries(next_followup_at)")


class EnquiryCreate(BaseModel):
    contact_name: str = Field(min_length=1, max_length=120)
    contact_phone: str = Field(min_length=5, max_length=30)
    service_category: str = Field(min_length=1, max_length=100)
    source: str = Field(default="staff_entry", max_length=80)
    next_followup_at: Optional[datetime] = None


class EnquiryUpdate(BaseModel):
    status: Optional[str] = None
    next_followup_at: Optional[datetime] = None


def require_api_key(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")):
    expected = os.getenv("PHANTOMOPS_API_KEY", "").strip()
    if not expected:
        raise HTTPException(status_code=503, detail="API key is not configured on this deployment.")
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid API key.")
    return True


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"ok": True, "service": "phantomops-healthcare-revenue-desk", "version": "0.1.0"}


@app.post("/api/enquiries", dependencies=[Depends(require_api_key)], status_code=201)
def create_enquiry(payload: EnquiryCreate):
    now = utc_now()
    enquiry_id = str(uuid.uuid4())
    followup = payload.next_followup_at.isoformat() if payload.next_followup_at else None
    with connect() as db:
        db.execute(
            """INSERT INTO enquiries
            (id, contact_name, contact_phone, service_category, source, status,
             next_followup_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'new', ?, ?, ?)""",
            (
                enquiry_id,
                payload.contact_name.strip(),
                payload.contact_phone.strip(),
                payload.service_category.strip(),
                payload.source.strip(),
                followup,
                now,
                now,
            ),
        )
    return {"id": enquiry_id, "status": "new", "created_at": now}


@app.get("/api/enquiries", dependencies=[Depends(require_api_key)])
def list_enquiries(
    status: Optional[str] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
):
    if status and status not in ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail="Unsupported enquiry status.")
    with connect() as db:
        if status:
            rows = db.execute(
                "SELECT * FROM enquiries WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                (status, limit),
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM enquiries ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
    return {"count": len(rows), "enquiries": [dict(row) for row in rows]}


@app.patch("/api/enquiries/{enquiry_id}", dependencies=[Depends(require_api_key)])
def update_enquiry(enquiry_id: str, payload: EnquiryUpdate):
    changes = {}
    if payload.status is not None:
        if payload.status not in ALLOWED_STATUSES:
            raise HTTPException(status_code=400, detail="Unsupported enquiry status.")
        changes["status"] = payload.status
    if payload.next_followup_at is not None:
        changes["next_followup_at"] = payload.next_followup_at.isoformat()
    if not changes:
        raise HTTPException(status_code=400, detail="No supported update fields supplied.")
    changes["updated_at"] = utc_now()
    assignments = ", ".join(f"{key} = ?" for key in changes)
    values = list(changes.values()) + [enquiry_id]
    with connect() as db:
        cursor = db.execute(f"UPDATE enquiries SET {assignments} WHERE id = ?", values)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Enquiry not found.")
    return {"id": enquiry_id, "updated": True, **changes}


@app.get("/api/metrics", dependencies=[Depends(require_api_key)])
def metrics():
    now = utc_now()
    with connect() as db:
        rows = db.execute("SELECT status, COUNT(*) AS total FROM enquiries GROUP BY status").fetchall()
        due = db.execute(
            """SELECT COUNT(*) AS total FROM enquiries
            WHERE next_followup_at IS NOT NULL AND next_followup_at <= ?
            AND status NOT IN ('completed', 'closed')""",
            (now,),
        ).fetchone()["total"]
        total = db.execute("SELECT COUNT(*) AS total FROM enquiries").fetchone()["total"]
    by_status = {row["status"]: row["total"] for row in rows}
    return {"total_enquiries": total, "by_status": by_status, "followups_due": due}
