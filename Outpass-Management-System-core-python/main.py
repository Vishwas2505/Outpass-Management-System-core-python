import sys
import os

# ensure project root on path so imports work from anywhere
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from service.auth_service import AuthService
from service.outpass_service import OutpassService
from service.attendance_service import AttendanceService
from service.gate_service import GateService
from service.violation_service import ViolationService
from service.report_service import ReportService

def main_menu():
    auth = AuthService()
    outpass = OutpassService()
    attendance = AttendanceService()
    gate = GateService()
    violation = ViolationService()
    report = ReportService()

    while True:
        print("\n==== OUTPASS MANAGEMENT SYSTEM ====")
        print("1. Register User")
        print("2. Login (by email)")
        print("3. Request Outpass")
        print("4. Approve Outpass")
        print("5. Reject Outpass")
        print("6. Mark Attendance")
        print("7. Record Gate Entry/Exit")
        print("8. Report Violation")
        print("9. Generate Summary Report")
        print("0. Exit")
        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                role = input("Role (student/warden/admin) [student]: ").strip() or "student"
                res = auth.register(name, email, role)
                print("Result:", getattr(res, "data", res))

            elif choice == "2":
                email = input("Email: ").strip()
                user = auth.login(email)
                print("Login successful." if user else "Login failed: user not found.")
                if user:
                    print(user)

            elif choice == "3":
                uid = int(input("User ID: ").strip())
                reason = input("Reason: ").strip()
                ftime = input("From Time (HH:MM): ").strip()
                ttime = input("To Time (HH:MM): ").strip()
                res = outpass.request_outpass(uid, reason, ftime, ttime)
                print("Requested:", getattr(res, "data", res))

            elif choice == "4":
                oid = int(input("Outpass ID to approve: ").strip())
                res = outpass.approve_outpass(oid)
                print("Approved:", getattr(res, "data", res))

            elif choice == "5":
                oid = int(input("Outpass ID to reject: ").strip())
                res = outpass.reject_outpass(oid)
                print("Rejected:", getattr(res, "data", res))

            elif choice == "6":
                uid = int(input("User ID: ").strip())
                status = input("Status (Present/Absent): ").strip()
                res = attendance.mark_attendance(uid, status)
                print("Attendance:", getattr(res, "data", res))

            elif choice == "7":
                uid = int(input("User ID: ").strip())
                action = input("Action (entry/exit): ").strip().lower()
                if action == "entry":
                    res = gate.record_entry(uid)
                else:
                    res = gate.record_exit(uid)
                print("Gate log:", getattr(res, "data", res))

            elif choice == "8":
                uid = int(input("User ID: ").strip())
                desc = input("Violation description: ").strip()
                res = violation.report_violation(uid, desc)
                print("Violation reported:", getattr(res, "data", res))

            elif choice == "9":
                print(report.system_summary())

            elif choice == "0":
                print("Exiting.")
                break

            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main_menu()
