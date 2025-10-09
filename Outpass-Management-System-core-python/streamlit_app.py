import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
from supabase_client import supabase

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(page_title="Outpass Management System", layout="wide")

st.title("🏫 Outpass Management System")

# -------------------- Helper Functions --------------------

def register_user(name, email, phone, department, role, password):
    """Insert new user into users table"""
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
    """Insert student and related user record"""
    user_res = register_user(name, email, phone, department, "student", password)

    if not user_res.data:
        return {"error": "Failed to create user"}

    user_id = user_res.data[0].get("user_id")

    # Fallback: fetch by email if Supabase doesn’t return ID
    if not user_id:
        existing = supabase.table("users").select("user_id").eq("email", email).execute()
        if existing.data:
            user_id = existing.data[0].get("user_id")

    if not user_id:
        return {"error": "User ID not found after insert"}

    student_res = supabase.table("students").insert({
        "user_id": user_id,
        "roll_no": roll_no
    }).execute()

    return {"user": user_res.data[0], "student": student_res.data[0]}


def register_warden(name, email, phone, department, password, employee_id):
    user_res = register_user(name, email, phone, department, "warden", password)
    if not user_res.data:
        return {"error": "Failed to create user"}

    user_id = user_res.data[0].get("user_id")
    if not user_id:
        existing = supabase.table("users").select("user_id").eq("email", email).execute()
        if existing.data:
            user_id = existing.data[0].get("user_id")

    warden_res = supabase.table("wardens").insert({
        "user_id": user_id,
        "employee_id": employee_id
    }).execute()
    return {"user": user_res.data[0], "warden": warden_res.data[0]}


def register_admin(name, email, phone, department, password):
    user_res = register_user(name, email, phone, department, "admin", password)
    if not user_res.data:
        return {"error": "Failed to create user"}

    user_id = user_res.data[0].get("user_id")
    admin_res = supabase.table("admins").insert({"user_id": user_id}).execute()
    return {"user": user_res.data[0], "admin": admin_res.data[0]}


# ------------- Utility Functions -------------
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


def get_all_outpasses_with_details():
    outpasses_res = supabase.table("outpasses").select("*").order("outpass_id", desc=True).execute()
    outpasses = outpasses_res.data or []
    rows = []
    for op in outpasses:
        stud = supabase.table("students").select("*").eq("student_id", op["student_id"]).execute().data
        student_user = {}
        if stud:
            user_id = stud[0]["user_id"]
            user = supabase.table("users").select("*").eq("user_id", user_id).execute().data
            if user:
                student_user = user[0]

        warden_user = {}
        if op.get("warden_id"):
            w = supabase.table("wardens").select("*").eq("warden_id", op["warden_id"]).execute().data
            if w:
                w_user = supabase.table("users").select("*").eq("user_id", w[0]["user_id"]).execute().data
                if w_user:
                    warden_user = w_user[0]

        rows.append({
            "outpass_id": op["outpass_id"],
            "student_name": student_user.get("name", ""),
            "warden_name": warden_user.get("name", ""),
            "reason": op.get("reason"),
            "from_date": op.get("from_date"),
            "to_date": op.get("to_date"),
            "status": op.get("status")
        })
    return rows


# -------------------- UI Section --------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_id = None

menu = st.sidebar.selectbox("Menu", ["Home", "Register", "Login", "Logout"])

if menu == "Home":
    st.write("Welcome to the Outpass Management System. Use the sidebar to Register or Login.")

elif menu == "Register":
    st.header("User Registration")
    role = st.selectbox("Role", ["student", "warden", "admin"])
    with st.form("reg_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        department = st.text_input("Department")
        password = st.text_input("Password", type="password")
        roll_no = st.text_input("Roll No") if role == "student" else None
        employee_id = st.text_input("Employee ID") if role == "warden" else None
        submitted = st.form_submit_button("Register")
        if submitted:
            if role == "student":
                res = register_student(name, email, phone, department, password, roll_no)
                if "student" in res:
                    st.success(f"Student registered successfully! Student ID: {res['student']['student_id']}")
                else:
                    st.error(str(res))
            elif role == "warden":
                res = register_warden(name, email, phone, department, password, employee_id)
                if "warden" in res:
                    st.success(f"Warden registered successfully! ID: {res['warden']['warden_id']}")
                else:
                    st.error(str(res))
            else:
                res = register_admin(name, email, phone, department, password)
                if "admin" in res:
                    st.success(f"Admin registered successfully! ID: {res['admin']['admin_id']}")
                else:
                    st.error(str(res))

elif menu == "Login":
    st.header("Login")
    role = st.selectbox("Login as", ["student", "warden", "admin"])
    user_id = st.number_input("Enter ID", min_value=1, step=1)
    if st.button("Login"):
        exists = (student_exists(user_id) if role == "student"
                  else warden_exists(user_id) if role == "warden"
                  else admin_exists(user_id))
        if exists:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.user_id = user_id
            st.success(f"Logged in as {role} #{user_id}")
        else:
            st.error(f"{role.title()} not found. Please register first.")

# -------------------- DASHBOARDS --------------------

if st.session_state.logged_in:

    role = st.session_state.role
    user_id = st.session_state.user_id

    if role == "student":
        st.subheader(f"Student Dashboard (ID: {user_id})")
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
                        st.error("Invalid Warden ID")
                    else:
                        res = apply_outpass(user_id, warden_id, reason, str(from_date), str(to_date))
                        if res.data:
                            st.success("Outpass Applied Successfully!")
                        else:
                            st.error("Failed to apply")
        elif action == "View My Outpasses":
            data = get_student_outpasses(user_id)
            st.table(data)
        elif action == "View Notifications":
            notes = get_notifications_for_student(user_id)
            st.table(notes)

    elif role == "warden":
        st.subheader(f"Warden Dashboard (ID: {user_id})")
        pendings = get_pending_for_warden(user_id)
        if not pendings:
            st.info("No pending outpasses.")
        else:
            for op in pendings:
                st.write(f"Outpass #{op['outpass_id']} | Student #{op['student_id']} | {op['reason']}")
                col1, col2 = st.columns(2)
                if col1.button(f"Approve {op['outpass_id']}", key=f"appr-{op['outpass_id']}"):
                    update_outpass_status(op['outpass_id'], "approved")
                    st.success("Approved")
                if col2.button(f"Reject {op['outpass_id']}", key=f"rej-{op['outpass_id']}"):
                    update_outpass_status(op['outpass_id'], "rejected")
                    st.error("Rejected")

    elif role == "admin":
        st.subheader(f"Admin Dashboard (ID: {user_id})")
        action = st.selectbox("Action", ["Add Student", "Generate Report"])
        if action == "Add Student":
            with st.form("add_student_form"):
                name = st.text_input("Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                department = st.text_input("Department")
                password = st.text_input("Password", type="password")
                roll_no = st.text_input("Roll No")
                submitted = st.form_submit_button("Add")
                if submitted:
                    res = register_student(name, email, phone, department, password, roll_no)
                    if "student" in res:
                        st.success(f"Added Student #{res['student']['student_id']}")
                    else:
                        st.error("Failed to add student")
        elif action == "Generate Report":
            import pandas as pd
            df = pd.DataFrame(get_all_outpasses_with_details())
            st.dataframe(df)

elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_id = None
    st.success("You have been logged out.")
