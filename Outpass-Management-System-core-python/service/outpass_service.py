from dao.outpass_dao import OutpassDAO

class OutpassService:
    def __init__(self):
        self.dao = OutpassDAO()

    def request_outpass(self, user_id: int, reason: str, from_time: str, to_time: str):
        return self.dao.create_outpass(user_id, reason, from_time, to_time)

    def approve_outpass(self, outpass_id: int):
        return self.dao.update_status(outpass_id, "Approved")

    def reject_outpass(self, outpass_id: int):
        return self.dao.update_status(outpass_id, "Rejected")

    def list_all(self):
        return self.dao.get_all_outpasses()

    def list_for_user(self, user_id: int):
        return self.dao.get_outpasses_by_user(user_id)
