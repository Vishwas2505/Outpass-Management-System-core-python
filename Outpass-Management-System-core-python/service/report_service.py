# service/report_service.py
from dao.report_dao import ReportDAO
from dao.outpass_dao import OutpassDAO

class ReportService:

    @staticmethod
    def generate_custom_report(report_type, content):
        return ReportDAO.generate_report(report_type, content)
    from dao.outpass_dao import OutpassDAO

    @staticmethod
    def generate_outpass_report():
        outpasses = OutpassDAO.get_all_outpasses()
        if outpasses.data:
            for op in outpasses.data:
                print(op)
        else:
            print("No outpasses found.")
        return outpasses

