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
        if "lease_owner" not in columns:
            self.conn.execute("ALTER TABLE missions ADD COLUMN lease_owner TEXT")
        if "lease_expires_at" not in columns:
            self.conn.execute("ALTER TABLE missions ADD COLUMN lease_expires_at TEXT")
        self.conn.commit()

    def now(self): return datetime.now(timezone.utc).isoformat()

    def event(self,kind,payload,mid=None):
        self.conn.execute("INSERT INTO events(mission_id,kind,payload,created_at) VALUES(?,?,?,?)",
            (mid,kind,json.dumps(payload,default=str),self.now()))
        self.conn.commit()

    def create_mission(self,goal):
        mid=str(uuid.uuid4()); n=self.now()
        self.conn.execute("INSERT INTO missions(id,goal,status,plan,result,created_at,updated_at,lease_owner,lease_expires_at) VALUES(?,?,?,?,?,?,?,?,?)",
            (mid,goal,"queued",None,None,n,n,None,None))
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

    def claim_mission(self,mid,owner,lease_seconds=None,statuses=None):
        if lease_seconds is None: lease_seconds=float(settings.mission_lease_seconds)
        statuses=tuple(statuses or ("running","retrying","blocked"))
        if not statuses: return False
        placeholders=",".join("?" for _ in statuses)
        now=datetime.now(timezone.utc); expires=(now+timedelta(seconds=lease_seconds)).isoformat()
        cursor=self.conn.execute(
            f"UPDATE missions SET lease_owner=?,lease_expires_at=?,updated_at=? "
            f"WHERE id=? AND status IN ({placeholders}) "
            "AND (lease_owner IS NULL OR lease_expires_at IS NULL OR lease_expires_at<=?)",
            (owner,expires,now.isoformat(),mid,*statuses,now.isoformat())
        )
        self.conn.commit()
        if cursor.rowcount:
            self.event("mission.lease_claimed",{"owner":owner,"expires_at":expires},mid)
            return True
        return False

    def release_mission(self,mid,owner):
        cursor=self.conn.execute(
            "UPDATE missions SET lease_owner=NULL,lease_expires_at=NULL,updated_at=? WHERE id=? AND lease_owner=?",
            (self.now(),mid,owner)
        )
        self.conn.commit()
        if cursor.rowcount:
            self.event("mission.lease_released",{"owner":owner},mid)
        return bool(cursor.rowcount)

    def list_resumable(self):
        rows=self.conn.execute(
            "SELECT * FROM missions WHERE status IN ('running','awaiting_approval','retrying','blocked') ORDER BY updated_at"
        ).fetchall()
        return [dict(r) for r in rows]

    def approval(self,mid,action,payload):
        marker=json.dumps(payload,sort_keys=True,default=str)
        existing=self.conn.execute(
            "SELECT * FROM approvals WHERE mission_id=? AND action=? AND status='pending' ORDER BY created_at DESC LIMIT 1",
            (mid,action)
        ).fetchone()
        if existing and json.dumps(json.loads(existing["payload"]),sort_keys=True,default=str)==marker:
            return existing["id"]
        aid=str(uuid.uuid4())
        try:
            self.conn.execute("INSERT INTO approvals VALUES(?,?,?,?,?,?,?)",
                (aid,mid,action,marker,"pending",self.now(),None))
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()
            existing=self.conn.execute(
                "SELECT * FROM approvals WHERE mission_id=? AND action=? AND payload=? AND status='pending' LIMIT 1",
                (mid,action,marker)
            ).fetchone()
            if existing:
                return existing["id"]
            raise
        self.event("approval.requested",{"approval_id":aid,"action":action},mid)
        return aid

    def pending_approval(self,mid):
        row=self.conn.execute(
            "SELECT * FROM approvals WHERE mission_id=? AND status='pending' ORDER BY created_at DESC LIMIT 1",
            (mid,)
        ).fetchone()
        return dict(row) if row else None

    def get_approval(self,aid):
        row=self.conn.execute("SELECT * FROM approvals WHERE id=?",(aid,)).fetchone()
        return dict(row) if row else None

    def resolve_approval(self,aid,status):
        if status not in ("approved","rejected"): raise ValueError(status)
        row=self.get_approval(aid)
        if not row: raise KeyError(aid)
        cursor=self.conn.execute(
            "UPDATE approvals SET status=?,resolved_at=? WHERE id=? AND status='pending'",
            (status,self.now(),aid)
        )
        self.conn.commit()
        if cursor.rowcount == 0:
            return None
        self.event("approval.resolved",{"approval_id":aid,"status":status},row["mission_id"])
        return self.get_approval(aid)
