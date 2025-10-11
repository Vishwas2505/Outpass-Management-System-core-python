from dao.outpass_dao import OutpassDAO
from dao.violation_dao import ViolationDAO
from collections import Counter

class ReportService:
    def __init__(self):
        self.outpass_dao = OutpassDAO()
        self.violation_dao = ViolationDAO()

    def system_summary(self):
        outpasses_resp = self.outpass_dao.get_all_outpasses()
        outpasses = outpasses_resp.data or []
        violations = (self.violation_dao.get_all_violations().data) or []
        statuses = [o.get("status") for o in outpasses]
        c = Counter(statuses)
        return {
            "total_outpasses": len(outpasses),
            "approved": c.get("Approved", 0),
            "pending": c.get("Pending", 0),
            "rejected": c.get("Rejected", 0),
            "total_violations": len(violations)
        }
