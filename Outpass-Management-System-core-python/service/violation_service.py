from dao.violation_dao import ViolationDAO

class ViolationService:
    def __init__(self):
        self.dao = ViolationDAO()

    def report_violation(self, user_id: int, description: str):
        return self.dao.report_violation(user_id, description)

    def list_violations(self):
        return self.dao.get_all_violations()
