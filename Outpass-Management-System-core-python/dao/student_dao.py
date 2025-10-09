from supabase_client import supabase

class StudentDAO:
    @staticmethod
    def add_student(user_id, roll_no):
        # Note: roll_no matches table column
        return supabase.table("students").insert({
            "user_id": user_id,
            "roll_no": roll_no
        }).execute()

    @staticmethod
    def get_student(student_id):
        return supabase.table("students").select("*").eq("student_id", student_id).execute()
