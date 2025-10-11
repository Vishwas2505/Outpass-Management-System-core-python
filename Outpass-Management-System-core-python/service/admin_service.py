from dao.user_dao import UserDAO
from dao.admin_dao import AdminDAO

class AdminService:
    @staticmethod
    def add_admin(name, email, phone, department, password):
        user_id = UserDAO.add_user(name, email, phone, department, "admin", password)
        return AdminDAO.add_admin(user_id)
