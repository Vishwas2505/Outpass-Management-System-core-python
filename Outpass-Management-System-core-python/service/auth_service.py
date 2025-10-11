from dao.user_dao import UserDAO

class AuthService:
    """
    Handles user authentication logic.
    """
    def __init__(self):
        self.user_dao = UserDAO()
