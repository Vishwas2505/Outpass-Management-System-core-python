from dao.user_dao import UserDAO

class AuthService:
    def __init__(self):
        self.user_dao = UserDAO()

    def register(self, name: str, email: str, role: str = "student"):
        # basic validation
        if not name or not email:
            raise ValueError("name and email required")
        existing = self.user_dao.get_user_by_email(email)
        if existing.data and len(existing.data) > 0:
            return existing  # return existing user info (up to you to handle)
        return self.user_dao.create_user(name, email, role)

    def login(self, email: str):
        res = self.user_dao.get_user_by_email(email)
        if res.data and len(res.data) > 0:
            return res.data[0]
        return None
