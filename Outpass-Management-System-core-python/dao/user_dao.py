from .db_config import get_supabase_client

class UserDAO:
    def __init__(self):
        self.client = get_supabase_client()

    def create_user(self, name: str, email: str, role: str = "student"):
        return self.client.table("users").insert({
            "name": name,
            "email": email,
            "role": role
        }).execute()

    def get_user_by_email(self, email: str):
        return self.client.table("users").select("*").eq("email", email).execute()

    def get_user_by_id(self, user_id: int):
        return self.client.table("users").select("*").eq("id", user_id).execute()

    def list_users(self):
        return self.client.table("users").select("*").execute()
