from dao.user_dao import UserDAO
from dao.warden_dao import WardenDAO

class WardenService:
    @staticmethod
    def add_warden(name, email, phone, department, password, employee_id):
        user_id = UserDAO.add_user(name, email, phone, department, "warden", password)
        return WardenDAO.add_warden(user_id, employee_id)
