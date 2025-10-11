# main.py
from service.user_service import UserService
from service.student_service import StudentService
from service.warden_service import WardenService
from service.admin_service import AdminService
from service.outpass_service import OutpassService
from service.notification_service import NotificationService
from service.report_service import ReportService


def register_menu():
    print("\n=== User Registration ===")
    role = input("Enter role (student/warden/admin): ").lower()
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    department = input("Department: ")
    password = input("Password: ")

    if role == "student":
        roll_no = input("Roll No: ")
        StudentService.add_student(name, email, phone, department, password, roll_no)
        print("Student registered successfully!")

    elif role == "warden":
        employee_id = input("Employee ID: ")
        WardenService.add_warden(name, email, phone, department, password, employee_id)
        print("Warden registered successfully!")

    elif role == "admin":
        AdminService.add_admin(name, email, phone, department, password)
        print("Admin registered successfully!")

    else:
        print("Invalid role  Registration failed")


def student_menu(student_id):
    while True:
        print("\n--Student Menu--")
        print("1. Apply for Outpass")
        print("2. View My Outpasses")
        print("3. View Notifications")
        print("4. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            warden_id = int(input("Warden ID: "))
            reason = input("Reason for Outpass: ")
            from_date = input("From Date (YYYY-MM-DD): ")
            to_date = input("To Date (YYYY-MM-DD): ")
            res = OutpassService.apply_outpass(student_id, warden_id, reason, from_date, to_date)
            print("Outpass applied:", res.data)

        elif choice == "2":
            outpasses = OutpassService.get_student_outpasses(student_id)
            if not outpasses:
                print("No outpasses found")
            else:
                for op in outpasses:
                    print(op)

        elif choice == "3":
            notifications = NotificationService.get_notifications(student_id)
            if not notifications:
                print("No notifications")
            else:
                for n in notifications:
                    print(n)

        elif choice == "4":
            break

        else:
            print("Invalid choice")


def warden_menu(warden_id):
    while True:
        print("\n--Warden Menu--")
        print("1. Approve Outpass")
        print("2. Reject Outpass")
        print("3. View Reports")
        print("4. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            outpass_id = int(input("Outpass ID to approve: "))
            OutpassService.approve_outpass(outpass_id)
            print("Outpass approved")

        elif choice == "2":
            outpass_id = int(input("Outpass ID to reject: "))
            OutpassService.reject_outpass(outpass_id)
            print("Outpass rejected")

        elif choice == "3":
            report = ReportService.generate_outpass_report()
            print("Report generated")

        elif choice == "4":
            break

        else:
            print("Invalid choice")


def admin_menu():
    while True:
        print("\n--Admin Menu--")
        print("1. Add Student")
        print("2. Add Warden")
        print("3. Add Admin")
        print("4. Generate Report")
        print("5. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            department = input("Department: ")
            password = input("Password: ")
            roll_no = input("Roll No: ")
            StudentService.add_student(name, email, phone, department, password, roll_no)
            print("Student added")

        elif choice == "2":
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            department = input("Department: ")
            password = input("Password: ")
            employee_id = input("Employee ID: ")
            WardenService.add_warden(name, email, phone, department, password, employee_id)
            print("Warden added")

        elif choice == "3":
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            department = input("Department: ")
            password = input("Password: ")
            AdminService.add_admin(name, email, phone, department, password)
            print("Admin added")

        elif choice == "4":
            report = ReportService.generate_outpass_report()
            print("Report generated")

        elif choice == "5":
            break

        else:
            print("Invalid choice. Try again.")


def main():
    while True:
        print("\n--Outpass Management System--")
        print("1. Register")
        print("2. Student Login")
        print("3. Warden Login")
        print("4. Admin Login")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            register_menu()

        elif choice == "2":
            student_id = int(input("Enter your Student ID: "))
            student_menu(student_id)

        elif choice == "3":
            warden_id = int(input("Enter your Warden ID: "))
            warden_menu(warden_id)

        elif choice == "4":
            admin_menu()

        elif choice == "5":
            print("Exiting")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
