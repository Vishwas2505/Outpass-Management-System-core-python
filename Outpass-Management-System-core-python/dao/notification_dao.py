from supabase_client import supabase

class NotificationDAO:
    @staticmethod
    def send_notification(outpass_id, message):
        return supabase.table("notifications").insert({
            "outpass_id": outpass_id,
            "message": message
        }).execute()

    @staticmethod
    def get_notifications_by_student(student_id):
        # First, get all outpasses for this student
        outpasses = supabase.table("outpasses").select("outpass_id").eq("student_id", student_id).execute()
        outpass_ids = [op["outpass_id"] for op in outpasses.data]
        if not outpass_ids:
            return []

        # Then get notifications for those outpass IDs
        return supabase.table("notifications").select("*").in_("outpass_id", outpass_ids).execute()
