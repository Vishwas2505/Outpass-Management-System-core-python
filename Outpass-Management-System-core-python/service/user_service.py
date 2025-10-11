# service/user_service.py
from dao.user_dao import UserDAO

class UserService:
    @staticmethod
    def add_user(name, email, phone, department, role, password):
        return UserDAO.add_user(name, email, phone, department, role, password)

    @staticmethod
    def get_user(email):
        return UserDAO.get_user_by_email(email)

    @staticmethod
    def update_user(user_id, update_data):
        return UserDAO.update_user(user_id, update_data)

    @staticmethod
    def delete_user(user_id):
        return UserDAO.delete_user(user_id)
