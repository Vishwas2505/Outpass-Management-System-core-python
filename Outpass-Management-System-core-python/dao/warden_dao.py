from supabase_client import supabase

class WardenDAO:
    @staticmethod
    def add_warden(user_id, employee_id):
        return supabase.table("wardens").insert({
            "user_id": user_id,
            "employee_id": employee_id
        }).execute()

    @staticmethod
    def get_warden(warden_id):
        return supabase.table("wardens").select("*").eq("warden_id", warden_id).execute()
