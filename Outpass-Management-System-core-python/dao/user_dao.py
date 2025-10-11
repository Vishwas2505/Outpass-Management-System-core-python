from dao.db_config import get_supabase_client

class UserDAO:
    def __init__(self):
        self.client = get_supabase_client()
        self.table = "users"  # Change if your table name is different

    def get_user_by_email(self, email):
        response = self.client.table(self.table).select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None

    def create_user(self, email, password):
        response = self.client.table(self.table).insert({"email": email, "password": password}).execute()
        return response.data
