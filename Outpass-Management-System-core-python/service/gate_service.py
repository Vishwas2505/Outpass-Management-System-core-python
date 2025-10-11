from dao.gate_dao import GateDAO

class GateService:
    def __init__(self):
        self.dao = GateDAO()

    def record_entry(self, user_id: int):
        return self.dao.log_entry(user_id, "entry")

    def record_exit(self, user_id: int):
        return self.dao.log_entry(user_id, "exit")

    def get_logs(self):
        return self.dao.get_logs()
