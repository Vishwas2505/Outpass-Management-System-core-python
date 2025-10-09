from supabase_client import supabase

class UserDAO:
    @staticmethod
    def add_user(name, email, phone, department, role, password):
        res = supabase.table("users").insert({
            "name": name,
            "email": email,
            "phone": phone,
            "department": department,
            "role": role,
            "password": password
        }).execute()
        # Return the inserted user's ID
        return res.data[0]["user_id"]

    @staticmethod
    def get_user(user_id):
        return supabase.table("users").select("*").eq("user_id", user_id).execute()
