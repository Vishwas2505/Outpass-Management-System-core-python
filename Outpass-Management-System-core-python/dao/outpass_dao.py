from .db_config import get_supabase_client
from datetime import datetime

class OutpassDAO:
    def __init__(self):
        self.client = get_supabase_client()

    def create_outpass(self, user_id: int, reason: str, from_time: str, to_time: str):
        return self.client.table("outpasses").insert({
            "user_id": user_id,
            "reason": reason,
            "from_time": from_time,
            "to_time": to_time,
            "status": "Pending",
            "created_at": datetime.utcnow().isoformat()
        }).execute()

    def update_status(self, outpass_id: int, status: str):
        return self.client.table("outpasses").update({"status": status}).eq("id", outpass_id).execute()

    def get_outpasses_by_user(self, user_id: int):
        return self.client.table("outpasses").select("*").eq("user_id", user_id).execute()

    def get_all_outpasses(self):
        return self.client.table("outpasses").select("*").execute()
