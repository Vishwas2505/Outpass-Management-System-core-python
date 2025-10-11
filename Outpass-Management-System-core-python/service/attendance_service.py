from dao.attendance_dao import AttendanceDAO

class AttendanceService:
    def __init__(self):
        self.dao = AttendanceDAO()

    def mark_attendance(self, user_id: int, status: str):
        return self.dao.mark_attendance(user_id, status)

    def get_attendance(self, user_id: int):
        return self.dao.get_attendance_by_user(user_id)
