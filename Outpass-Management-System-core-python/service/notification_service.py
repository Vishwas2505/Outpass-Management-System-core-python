from dao.notification_dao import NotificationDAO

class NotificationService:
    @staticmethod
    def send_notification(outpass_id, message):
        return NotificationDAO.send_notification(outpass_id, message)

    @staticmethod
    def get_notifications(student_id):
        return NotificationDAO.get_notifications_by_student(student_id)
 