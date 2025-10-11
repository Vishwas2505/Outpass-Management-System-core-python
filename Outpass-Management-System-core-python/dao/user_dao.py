from dao.db_config import get_supabase_client

class UserDAO:
    """
    Data Access Object for user-related database operations.
    Uses Supabase client safely with Streamlit Cloud secrets.
    """
    def __init__(self):
        self.client = get_supabase_client()
        self.table_name = "users"  # Make sure your Supabase table is named 'users'

    def get_user_by_email(self, email: str):
        """
        Fetch a user by email.
        Returns None if not found.
        """
        response = self.client.table(self.table_name).select("*").eq("email", email).execute()
        data = response.data
        if data and len(data) > 0:
            return data[0]
        return None

    def create_user(self, user_dict: dict):
        """
        Create a new user in the database.
        user_dict should have all required fields: {"email": ..., "name": ..., etc.}
        """
        response = self.client.table(self.table_name).insert(user_dict).execute()
        return response.data

    def update_user(self, email: str, updates: dict):
        """
        Update user details by email.
        """
        response = self.client.table(self.table_name).update(updates).eq("email", email).execute()
        return response.data

    def delete_user(self, email: str):
        """
        Delete a user by email.
        """
        response = self.client.table(self.table_name).delete().eq("email", email).execute()
        return response.data
