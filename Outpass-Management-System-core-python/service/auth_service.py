from dao.user_dao import UserDAO

class AuthService:
    def __init__(self):
        self.user_dao = UserDAO()

    def login(self, email, password):
        user = self.user_dao.get_user_by_email(email)
        if user and user["password"] == password:
            return True
        return False

    def register(self, email, password):
        return self.user_dao.create_user(email, password)
