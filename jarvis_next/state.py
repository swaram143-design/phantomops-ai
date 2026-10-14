import json,os,sqlite3,uuid
from datetime import datetime,timezone,timedelta
from .config import settings

class StateStore:
    def __init__(self,path=None):
        self.path=path or settings.db_path
        os.makedirs(os.path.dirname(self.path) or ".",exist_ok=True)
        self.conn=sqlite3.connect(self.path,check_same_thread=False)
        self.conn.row_factory=sqlite3.Row
        self.conn.execute("PRAGMA busy_timeout=5000")
        self.conn.executescript("""CREATE TABLE IF NOT EXISTS missions(id TEXT PRIMARY KEY,goal TEXT,status TEXT,plan TEXT,result TEXT,created_at TEXT,updated_at TEXT);
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,mission_id TEXT,kind TEXT,payload TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS approvals(id TEXT PRIMARY KEY,mission_id TEXT,action TEXT,payload TEXT,status TEXT,created_at TEXT,resolved_at TEXT);
CREATE UNIQUE INDEX IF NOT EXISTS idx_pending_approval_dedupe
ON approvals(mission_id,action,payload) WHERE status='pending';""")
        columns={row[1] for row in self.conn.execute("PRAGMA table_info(missions)").fetchall()}
        if "lease_owner" not in columns: self.conn.execute("ALTER TABLE missions ADD COLUMN lease_owner TEXT")
        if "lease_expires_at" not in columns: self.conn.execute("ALTER TABLE missions ADD COLUMN lease_expires_at TEXT")
        self.conn.commit()
    def now(self): return datetime.now(timezone.utc).isoformat()
    def _insert_event(self,kind,payload,mid=None): self.conn.execute("INSERT INTO events(mission_id,kind,payload,created_at) VALUES(?,?,?,?)",(mid,kind,json.dumps(payload,default=str),self.now()))
    def event(self,kind,payload,mid=None,lease_owner=None):
        try:
            if lease_owner is None:
                self._insert_event(kind,payload,mid); self.conn.commit(); return True
            cursor=self.conn.execute("UPDATE missions SET updated_at=? WHERE id=? AND lease_owner=? AND lease_expires_at>?",(self.now(),mid,lease_owner,self.now()))
            if cursor.rowcount == 0:
                self.conn.rollback(); return False
            self._insert_event(kind,payload,mid); self.conn.commit(); return True
        except Exception:
            self.conn.rollback(); raise
    def create_mission(self,goal):
        mid=str(uuid.uuid4()); n=self.now()
        try:
            self.conn.execute("INSERT INTO missions(id,goal,status,plan,result,created_at,updated_at,lease_owner,lease_expires_at) VALUES(?,?,?,?,?,?,?,?,?)",(mid,goal,"queued",None,None,n,n,None,None)); self._insert_event("mission.created",{"goal":goal},mid); self.conn.commit()
        except Exception: self.conn.rollback(); raise
        return mid
    def update(self,mid,status=None,plan=None,result=None,lease_owner=None): return self.update_with_event(mid,status=status,plan=plan,result=result,lease_owner=lease_owner)
    def update_with_event(self,mid,status=None,plan=None,result=None,lease_owner=None,event_kind=None,event_payload=None):
        row=self.conn.execute("SELECT * FROM missions WHERE id=?",(mid,)).fetchone()
        if not row: raise KeyError(mid)
        values=(status or row["status"],json.dumps(plan,default=str) if plan is not None else row["plan"],json.dumps(result,default=str) if result is not None else row["result"],self.now(),mid)
        try:
            if lease_owner is None: cursor=self.conn.execute("UPDATE missions SET status=?,plan=?,result=?,updated_at=? WHERE id=?",values)
            else: cursor=self.conn.execute("UPDATE missions SET status=?,plan=?,result=?,updated_at=? WHERE id=? AND lease_owner=? AND lease_expires_at>?",values+(lease_owner,self.now()))
            if lease_owner is not None and cursor.rowcount == 0: self.conn.rollback(); raise RuntimeError("mission lease lost")
            self._insert_event("mission.updated",{"status":status},mid)
            if event_kind: self._insert_event(event_kind,event_payload or {},mid)
            self.conn.commit()
        except Exception: self.conn.rollback(); raise
    def reconcile_uncertain_transition(self,mid,expected_result,plan,result,event_payload):
        """Compare-and-swap an uncertain failed mission into running exactly once."""
        plan_json=json.dumps(plan,default=str); result_json=json.dumps(result,default=str); now=self.now()
        try:
            cursor=self.conn.execute("UPDATE missions SET status='running',plan=?,result=?,updated_at=? WHERE id=? AND status='failed' AND result=?",(plan_json,result_json,now,mid,expected_result))
            if cursor.rowcount == 0:
                self.conn.rollback()
                return False
            self._insert_event("mission.updated",{"status":"running"},mid)
            self._insert_event("worker.uncertain_reconciled",event_payload or {},mid)
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            raise
    def get_mission(self,mid):
        row=self.conn.execute("SELECT * FROM missions WHERE id=?",(mid,)).fetchone(); return dict(row) if row else None
    def has_mission_lease(self,mid,owner):
        row=self.conn.execute("SELECT lease_owner,lease_expires_at FROM missions WHERE id=?",(mid,)).fetchone()
        if not row or row["lease_owner"] != owner or not row["lease_expires_at"]: return False
        try: return datetime.fromisoformat(row["lease_expires_at"]) > datetime.now(timezone.utc)
        except ValueError: return False
    def claim_mission(self,mid,owner,lease_seconds=None,statuses=None):
        if lease_seconds is None: lease_seconds=float(settings.mission_lease_seconds)
        statuses=tuple(statuses or ("running","retrying","blocked"))
        if not statuses: return False
        placeholders=",".join("?" for _ in statuses); now=datetime.now(timezone.utc); expires=(now+timedelta(seconds=lease_seconds)).isoformat()
        try:
            cursor=self.conn.execute(f"UPDATE missions SET lease_owner=?,lease_expires_at=?,updated_at=? WHERE id=? AND status IN ({placeholders}) AND (lease_owner IS NULL OR lease_expires_at IS NULL OR lease_expires_at<=?)",(owner,expires,now.isoformat(),mid,*statuses,now.isoformat()))
            if cursor.rowcount: self._insert_event("mission.lease_claimed",{"owner":owner,"expires_at":expires},mid); self.conn.commit(); return True
            self.conn.rollback(); return False
        except Exception: self.conn.rollback(); raise
    def renew_mission(self,mid,owner,lease_seconds=None):
        if lease_seconds is None: lease_seconds=float(settings.mission_lease_seconds)
        now=datetime.now(timezone.utc); expires=(now+timedelta(seconds=lease_seconds)).isoformat()
        try:
            cursor=self.conn.execute("UPDATE missions SET lease_expires_at=?,updated_at=? WHERE id=? AND lease_owner=? AND lease_expires_at>?",(expires,now.isoformat(),mid,owner,now.isoformat())); self.conn.commit(); return bool(cursor.rowcount)
        except Exception: self.conn.rollback(); raise
    def release_mission(self,mid,owner):
        try:
            cursor=self.conn.execute("UPDATE missions SET lease_owner=NULL,lease_expires_at=NULL,updated_at=? WHERE id=? AND lease_owner=?",(self.now(),mid,owner))
            if cursor.rowcount: self._insert_event("mission.lease_released",{"owner":owner},mid)
            self.conn.commit(); return bool(cursor.rowcount)
        except Exception: self.conn.rollback(); raise
    def list_resumable(self):
        rows=self.conn.execute("SELECT * FROM missions WHERE status IN ('running','awaiting_approval','retrying','blocked') ORDER BY updated_at").fetchall(); return [dict(r) for r in rows]
    def approval(self,mid,action,payload):
        marker=json.dumps(payload,sort_keys=True,default=str); existing=self.conn.execute("SELECT * FROM approvals WHERE mission_id=? AND action=? AND status='pending' ORDER BY created_at DESC LIMIT 1",(mid,action)).fetchone()
        if existing and json.dumps(json.loads(existing["payload"]),sort_keys=True,default=str)==marker: return existing["id"]
        aid=str(uuid.uuid4())
        try:
            self.conn.execute("INSERT INTO approvals VALUES(?,?,?,?,?,?,?)",(aid,mid,action,marker,"pending",self.now(),None)); self._insert_event("approval.requested",{"approval_id":aid,"action":action},mid); self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback(); existing=self.conn.execute("SELECT * FROM approvals WHERE mission_id=? AND action=? AND payload=? AND status='pending' LIMIT 1",(mid,action,marker)).fetchone()
            if existing: return existing["id"]
            raise
        except Exception: self.conn.rollback(); raise
        return aid
    def pending_approval(self,mid):
        row=self.conn.execute("SELECT * FROM approvals WHERE mission_id=? AND status='pending' ORDER BY created_at DESC LIMIT 1",(mid,)).fetchone(); return dict(row) if row else None
    def get_approval(self,aid):
        row=self.conn.execute("SELECT * FROM approvals WHERE id=?",(aid,)).fetchone(); return dict(row) if row else None
    def resolve_approval(self,aid,status,lease_owner=None):
        if status not in ("approved","rejected"): raise ValueError(status)
        row=self.get_approval(aid)
        if not row: raise KeyError(aid)
        mission=self.get_mission(row["mission_id"])
        if not mission or not mission.get("plan"):
            raise ValueError("Approval no longer matches a stored mission plan")
        try:
            payload=json.loads(row["payload"] or "{}")
            plan=json.loads(mission["plan"] or "{}")
            step_index=int(payload.get("step_index",-1))
            steps=plan.get("steps",[])
            if step_index < 0 or step_index >= len(steps):
                raise ValueError("Approval no longer matches the stored mission plan")
            planned_step=steps[step_index]
            if payload.get("step") != planned_step or row["action"] != planned_step.get("action"):
                raise ValueError("Approval no longer matches the stored mission plan")
        except (TypeError,ValueError,KeyError,json.JSONDecodeError):
            raise ValueError("Approval no longer matches the stored mission plan")
        now=datetime.now(timezone.utc); now_iso=now.isoformat()
        try:
            if lease_owner is not None:
                lease_cursor=self.conn.execute("UPDATE missions SET status=?,updated_at=? WHERE id=? AND status='awaiting_approval' AND lease_owner=? AND lease_expires_at>?",("running" if status == "approved" else "rejected",now_iso,row["mission_id"],lease_owner,now_iso))
                if lease_cursor.rowcount == 0:
                    self.conn.rollback(); return None
            elif mission["status"] == "awaiting_approval" and mission.get("lease_owner") and mission.get("lease_expires_at"):
                lease_cursor=self.conn.execute("UPDATE missions SET status=?,updated_at=? WHERE id=? AND status='awaiting_approval' AND lease_owner=? AND lease_expires_at>?",("running" if status == "approved" else "rejected",now_iso,row["mission_id"],mission["lease_owner"],now_iso))
                if lease_cursor.rowcount == 0:
                    self.conn.rollback(); return None
            cursor=self.conn.execute("UPDATE approvals SET status=?,resolved_at=? WHERE id=? AND status='pending'",(status,now_iso,aid))
            if cursor.rowcount == 0: self.conn.rollback(); return None
            self._insert_event("approval.resolved",{"approval_id":aid,"status":status},row["mission_id"]); self.conn.commit(); return self.get_approval(aid)
        except Exception: self.conn.rollback(); raise
