from dao.outpass_dao import OutpassDAO

class OutpassService:

    @staticmethod
    def apply_outpass(student_id, warden_id, reason, from_date, to_date):
        return OutpassDAO.apply_outpass(student_id, warden_id, reason, from_date, to_date)

    @staticmethod
    def get_student_outpasses(student_id):
        return OutpassDAO.get_student_outpasses(student_id)

    @staticmethod
    def approve_outpass(outpass_id):
        return OutpassDAO.update_status(outpass_id, "approved")

    @staticmethod
    def reject_outpass(outpass_id):
        return OutpassDAO.update_status(outpass_id, "rejected")
