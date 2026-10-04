import json,os,sqlite3,uuid
from datetime import datetime,timezone
from .config import settings

class StateStore:
    def __init__(self,path=None):
        self.path=path or settings.db_path
        os.makedirs(os.path.dirname(self.path) or ".",exist_ok=True)
        self.conn=sqlite3.connect(self.path,check_same_thread=False)
        self.conn.row_factory=sqlite3.Row
        self.conn.executescript("""CREATE TABLE IF NOT EXISTS missions(id TEXT PRIMARY KEY,goal TEXT,status TEXT,plan TEXT,result TEXT,created_at TEXT,updated_at TEXT);
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,mission_id TEXT,kind TEXT,payload TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS approvals(id TEXT PRIMARY KEY,mission_id TEXT,action TEXT,payload TEXT,status TEXT,created_at TEXT,resolved_at TEXT);""")
        self.conn.commit()

    def now(self): return datetime.now(timezone.utc).isoformat()

    def event(self,kind,payload,mid=None):
        self.conn.execute("INSERT INTO events(mission_id,kind,payload,created_at) VALUES(?,?,?,?)",
            (mid,kind,json.dumps(payload,default=str),self.now()))
        self.conn.commit()

    def create_mission(self,goal):
        mid=str(uuid.uuid4()); n=self.now()
        self.conn.execute("INSERT INTO missions VALUES(?,?,?,?,?,?,?)",
            (mid,goal,"queued",None,None,n,n))
        self.conn.commit()
        self.event("mission.created",{"goal":goal},mid)
        return mid

    def update(self,mid,status=None,plan=None,result=None):
        row=self.conn.execute("SELECT * FROM missions WHERE id=?",(mid,)).fetchone()
        if not row: raise KeyError(mid)
        self.conn.execute("UPDATE missions SET status=?,plan=?,result=?,updated_at=? WHERE id=?",
            (status or row["status"],
             json.dumps(plan,default=str) if plan is not None else row["plan"],
             json.dumps(result,default=str) if result is not None else row["result"],
             self.now(),mid))
        self.conn.commit()
        self.event("mission.updated",{"status":status},mid)

    def get_mission(self,mid):
        row=self.conn.execute("SELECT * FROM missions WHERE id=?",(mid,)).fetchone()
        return dict(row) if row else None

    def list_resumable(self):
        rows=self.conn.execute(
            "SELECT * FROM missions WHERE status IN ('running','awaiting_approval','retrying','blocked') ORDER BY updated_at"
        ).fetchall()
        return [dict(r) for r in rows]

    def approval(self,mid,action,payload):
        # JARVIS-NEXT is the canonical approval authority. Reuse an existing
        # pending approval for the same mission/step instead of creating
        # duplicate approval requests after retries or process restarts.
        marker=json.dumps(payload,sort_keys=True,default=str)
        existing=self.conn.execute(
            "SELECT * FROM approvals WHERE mission_id=? AND action=? AND status='pending' ORDER BY created_at DESC LIMIT 1",
            (mid,action)
        ).fetchone()
        if existing and json.dumps(json.loads(existing["payload"]),sort_keys=True,default=str)==marker:
            return existing["id"]

        aid=str(uuid.uuid4())
        self.conn.execute("INSERT INTO approvals VALUES(?,?,?,?,?,?,?)",
            (aid,mid,action,marker,"pending",self.now(),None))
        self.conn.commit()
        self.event("approval.requested",{"approval_id":aid,"action":action},mid)
        return aid

    def get_approval(self,aid):
        row=self.conn.execute("SELECT * FROM approvals WHERE id=?",(aid,)).fetchone()
        return dict(row) if row else None

    def resolve_approval(self,aid,status):
        if status not in ("approved","rejected"): raise ValueError(status)
        row=self.get_approval(aid)
        if not row: raise KeyError(aid)
        if row["status"]!="pending":
            return row
        self.conn.execute("UPDATE approvals SET status=?,resolved_at=? WHERE id=?",
            (status,self.now(),aid))
        self.conn.commit()
        self.event("approval.resolved",{"approval_id":aid,"status":status},row["mission_id"])
        return self.get_approval(aid)
