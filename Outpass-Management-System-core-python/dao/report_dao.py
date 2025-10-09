from supabase_client import supabase

class ReportDAO:
    @staticmethod
    def generate_report(report_type, content):
        return supabase.table("reports").insert({
            "report_type": report_type, "content": content
        }).execute()
