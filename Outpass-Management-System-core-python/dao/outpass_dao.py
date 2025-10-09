from supabase_client import supabase

class OutpassDAO:

    @staticmethod
    def apply_outpass(student_id, warden_id, reason, from_date, to_date):
        return supabase.table("outpasses").insert({
            "student_id": student_id,
            "warden_id": warden_id,
            "reason": reason,
            "from_date": from_date,
            "to_date": to_date
        }).execute()

    @staticmethod
    def get_student_outpasses(student_id):
        # Fetch all outpasses for a specific student
        return supabase.table("outpasses").select("*").eq("student_id", student_id).execute()

    @staticmethod
    def get_all_outpasses():
        # Fetch all outpasses for admin reports
        return supabase.table("outpasses").select("*").execute()

    @staticmethod
    def update_status(outpass_id, status):
        return supabase.table("outpasses").update({"status": status}).eq("outpass_id", outpass_id).execute()
