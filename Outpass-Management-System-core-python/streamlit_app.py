# streamlit_app.py
import streamlit as st
from datetime import datetime
from supabase_client import supabase  # Make sure supabase_client.py is correctly configured

# -------------------- Page Config -------------------- #
st.set_page_config(page_title="Outpass Management System", layout="wide")

# -------------------- Session State -------------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_id = None

# -------------------- Helper Functions -------------------- #

def register_user(name, email, phone, department, role, password):
    res = supabase.table("users").insert({
        "name": name,
        "email": email,
        "phone": phone,
        "department": department,
        "role": role,
        "password": password
    }).execute()
    return res

def register_student(name, email, phone, department, password, roll_no):
    user_res = register_user(name, email, phone, department, "student", password)
    if not user_res.data:
        return {"error": "Failed to create user"}
    user_id = user_res.data[0]["user_id"]
    student_res = supabase.table("students").insert({
        "user_id": user_id,
        "roll_no": roll_no
    }).execute()
    return {"user": user_res.data[0], "student": student_res.data[0]}

def register_warden(name, email, phone, department, password, employee_id):
    user_res = register_user(name, email, phone, department, "warden", password)
    if not user_res.data:
        return {"error": "Failed to create user"}
    user_id = user_res.data[0]["user_id"]
    warden_res = supabase.table("wardens").insert({
        "user_id": user_id,
        "employee_id": employee_id
    }).execute()
    return {"user": user_res.data[0], "warden": warden_res.data[0]}

def register_admin(name, email, phone, department, password):
    user_res = register_user(name, email, phone, department, "admin", password)
    if not user_res.data:
        return {"error": "Failed to create user"}
    user_id = user_res.data[0]["user_id"]
    admin_res = supabase.table("admins").insert({"user_id": user_id}).execute()
    return {"user": user_res.data[0], "admin": admin_res.data[0]}

def student_exists(student_id):
    r = supabase.table("students").select("*").eq("student_id", student_id).execute()
    return bool(r.data)

def warden_exists(warden_id):
    r = supabase.table("wardens").select("*").eq("warden_id", warden_id).execute()
    return bool(r.data)

def admin_exists(admin_id):
    r = supabase.table("admins").select("*").eq("admin_id", admin_id).execute()
    return bool(r.data)

def apply_outpass(student_id, warden_id, reason, from_date, to_date):
    r = supabase.table("outpasses").insert({
        "student_id": student_id,
        "warden_id": warden_id,
        "reason": reason,
        "from_date": from_date,
        "to_date": to_date,
        "status": "pending"
    }).execute()
    if r.data:
        supabase.table("notifications").insert({
            "outpass_id": r.data[0]["outpass_id"],
            "message": "Outpass applied - pending"
        }).execute()
    return r

def get_student_outpasses(student_id):
    r = supabase.table("outpasses").select("*").eq("student_id", student_id).order("outpass_id", desc=True).execute()
    return r.data if r.data else []

def get_notifications_for_student(student_id):
    outs = supabase.table("outpasses").select("outpass_id").eq("student_id", student_id).execute()
    if not outs.data:
        return []
    ids = [o["outpass_id"] for o in outs.data]
    n = supabase.table("notifications").select("*").in_("outpass_id", ids).order("notification_id", desc=True).execute()
    return n.data if n.data else []

def get_pending_for_warden(warden_id):
    r = supabase.table("outpasses").select("*").eq("warden_id", warden_id).eq("status", "pending").execute()
    return r.data if r.data else []

def update_outpass_status(outpass_id, status):
    r = supabase.table("outpasses").update({"status": status}).eq("outpass_id", outpass_id).execute()
    if r.data:
        supabase.table("notifications").insert({
            "outpass_id": outpass_id,
            "message": f"Outpass {status}"
        }).execute()
    return r

# -------------------- Sidebar Menu -------------------- #
menu = st.sidebar.selectbox("Menu", ["Home", "Register", "Login"])

# -------------------- Home -------------------- #
if menu == "Home":
    st.write("Welcome to the Outpass Management System! Use the sidebar to Register or Login.")

# -------------------- Registration -------------------- #
if menu == "Register":
    st.header("User Registration")
    role = st.selectbox("Role", ["student", "warden", "admin"])
    with st.form("reg_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        department = st.text_input("Department")
        password = st.text_input("Password", type="password")
        if role == "student":
            roll_no = st.text_input("Roll No")
        elif role == "warden":
            employee_id = st.text_input("Employee ID")
        else:
            roll_no = employee_id = None

        submitted = st.form_submit_button("Register")
        if submitted:
            if role == "student":
                res = register_student(name, email, phone, department, password, roll_no)
            elif role == "warden":
                res = register_warden(name, email, phone, department, password, employee_id)
            else:
                res = register_admin(name, email, phone, department, password)
            st.json(res)

# -------------------- Login -------------------- #
if menu == "Login":
    st.header("Login")
    if st.session_state.logged_in:
        st.success(f"Logged in as {st.session_state.user_role.capitalize()} (ID: {st.session_state.user_id})")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.user_id = None
            st.experimental_rerun()
    else:
        role = st.selectbox("Login as", ["student", "warden", "admin"])
        user_id_input = st.number_input(f"{role.capitalize()} ID", min_value=1, step=1)
        if st.button(f"Login as {role.capitalize()}"):
            exists = False
            if role == "student":
                exists = student_exists(user_id_input)
            elif role == "warden":
                exists = warden_exists(user_id_input)
            elif role == "admin":
                exists = admin_exists(user_id_input)
            if exists:
                st.session_state.logged_in = True
                st.session_state.user_role = role
                st.session_state.user_id = user_id_input
                st.experimental_rerun()
            else:
                st.error(f"{role.capitalize()} not found. Please register first.")

# -------------------- Dashboards -------------------- #
if st.session_state.logged_in:
    role = st.session_state.user_role
    user_id = st.session_state.user_id

    if role == "student":
        st.subheader("Student Dashboard")
        st.write(f"Logged in as Student ID: {user_id}")
        action = st.selectbox("Action", ["Apply Outpass", "View My Outpasses", "View Notifications"])
        
        if action == "Apply Outpass":
            with st.form("apply_form"):
                warden_id = st.number_input("Warden ID", min_value=1, step=1)
                reason = st.text_area("Reason")
                from_date = st.date_input("From Date")
                to_date = st.date_input("To Date")
                submit_apply = st.form_submit_button("Apply")
                if submit_apply:
                    if not warden_exists(warden_id):
                        st.error("Warden ID not found.")
                    else:
                        res = apply_outpass(user_id, warden_id, reason, str(from_date), str(to_date))
                        st.success(f"Outpass applied. ID: {res.data[0]['outpass_id']}")

        elif action == "View My Outpasses":
            data = get_student_outpasses(user_id)
            st.table(data)
        elif action == "View Notifications":
            notes = get_notifications_for_student(user_id)
            st.table(notes)

    elif role == "warden":
        st.subheader("Warden Dashboard")
        st.write(f"Logged in as Warden ID: {user_id}")
        pendings = get_pending_for_warden(user_id)
        if not pendings:
            st.info("No pending outpasses.")
        else:
            for op in pendings:
                st.write(f"Outpass ID: {op['outpass_id']} | Student ID: {op['student_id']} | Reason: {op['reason']} | From: {op['from_date']} | To: {op['to_date']}")
                cols = st.columns(2)
                if cols[0].button(f"Approve-{op['outpass_id']}", key=f"appr-{op['outpass_id']}"):
                    update_outpass_status(op['outpass_id'], "approved")
                    st.success(f"Approved outpass {op['outpass_id']}")
                if cols[1].button(f"Reject-{op['outpass_id']}", key=f"rej-{op['outpass_id']}"):
                    update_outpass_status(op['outpass_id'], "rejected")
                    st.success(f"Rejected outpass {op['outpass_id']}")

    elif role == "admin":
        st.subheader("Admin Dashboard")
        st.write(f"Logged in as Admin ID: {user_id}")

        admin_action = st.selectbox("Admin Actions", [
            "View All Students",
            "View All Wardens",
            "View All Admins",
            "View All Outpasses"
        ])

        if admin_action == "View All Students":
            students = supabase.table("students").select("*").execute()
            if students.data:
                st.table(students.data)
            else:
                st.info("No students found.")

        elif admin_action == "View All Wardens":
            wardens = supabase.table("wardens").select("*").execute()
            if wardens.data:
                st.table(wardens.data)
            else:
                st.info("No wardens found.")

        elif admin_action == "View All Admins":
            admins = supabase.table("admins").select("*").execute()
            if admins.data:
                st.table(admins.data)
            else:
                st.info("No admins found.")

        elif admin_action == "View All Outpasses":
            outpasses = supabase.table("outpasses").select("*").execute()
            if outpasses.data:
                st.table(outpasses.data)
            else:
                st.info("No outpasses found.")

