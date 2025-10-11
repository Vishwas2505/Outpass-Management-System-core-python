from .db_config import get_supabase_client
from datetime import datetime

class ViolationDAO:
    def __init__(self):
        self.client = get_supabase_client()

    def report_violation(self, user_id: int, description: str):
        return self.client.table("violations").insert({
            "user_id": user_id,
            "description": description,
            "reported_at": datetime.utcnow().isoformat()
        }).execute()

    def get_all_violations(self):
        return self.client.table("violations").select("*").execute()
