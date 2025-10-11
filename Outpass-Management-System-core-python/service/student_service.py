from dao.user_dao import UserDAO
from dao.student_dao import StudentDAO

class StudentService:
    @staticmethod
    def add_student(name, email, phone, department, password, roll_no):
        user_id = UserDAO.add_user(name, email, phone, department, "student", password)
        return StudentDAO.add_student(user_id, roll_no)

    @staticmethod
    def get_student(student_id):
        return StudentDAO.get_student(student_id)
