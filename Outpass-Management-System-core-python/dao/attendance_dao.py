from .db_config import get_supabase_client
from datetime import datetime

class AttendanceDAO:
    def __init__(self):
        self.client = get_supabase_client()

    def mark_attendance(self, user_id: int, status: str):
        return self.client.table("attendance").insert({
            "user_id": user_id,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }).execute()

    def get_attendance_by_user(self, user_id: int):
        return self.client.table("attendance").select("*").eq("user_id", user_id).execute()
