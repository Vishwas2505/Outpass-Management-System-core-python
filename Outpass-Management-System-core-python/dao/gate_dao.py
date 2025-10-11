from .db_config import get_supabase_client
from datetime import datetime

class GateDAO:
    def __init__(self):
        self.client = get_supabase_client()

    def log_entry(self, user_id: int, action: str):
        return self.client.table("gate_logs").insert({
            "user_id": user_id,
            "action": action,
            "timestamp": datetime.utcnow().isoformat()
        }).execute()

    def get_logs(self):
        return self.client.table("gate_logs").select("*").execute()
