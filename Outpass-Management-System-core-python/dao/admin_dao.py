from supabase_client import supabase

class AdminDAO:
    @staticmethod
    def add_admin(user_id):
        return supabase.table("admins").insert({"user_id": user_id}).execute()

    @staticmethod
    def get_admin(admin_id):
        return supabase.table("admins").select("*").eq("admin_id", admin_id).execute()
