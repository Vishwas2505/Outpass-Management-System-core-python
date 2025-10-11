import sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import streamlit as st
from datetime import time
from service.auth_service import AuthService
from service.outpass_service import OutpassService
from service.attendance_service import AttendanceService
from service.gate_service import GateService
from service.violation_service import ViolationService
from service.report_service import ReportService

st.set_page_config(page_title="Outpass Management System", layout="wide")
st.title("🏫 Outpass Management System")

# Initialize services
auth_service = AuthService()
outpass_service = OutpassService()
attendance_service = AttendanceService()
gate_service = GateService()
violation_service = ViolationService()
report_service = ReportService()

# Safe rerun helper
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# Sidebar: register/login
st.sidebar.header("Account")
action = st.sidebar.radio("Action", ["Login", "Register"])
if action == "Register":
    name = st.sidebar.text_input("Full name")
    email = st.sidebar.text_input("Email")
    role = st.sidebar.selectbox("Role", ["student", "warden", "admin"])
    if st.sidebar.button("Register"):
        try:
            auth_service.register(name, email, role)
            st.sidebar.success("Registered successfully!")
        except Exception as e:
            st.sidebar.error(str(e))
elif action == "Login":
    email = st.sidebar.text_input("Email for login")
    if st.sidebar.button("Login"):
        user = auth_service.login(email)
        if user:
            st.session_state["user"] = user
            st.sidebar.success(f"Logged in as {user['name']} ({user['role']})")
        else:
            st.sidebar.error("User not found")

# Main UI
if "user" in st.session_state:
    user = st.session_state["user"]
    role = user.get("role", "student")
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.pop("user")
        safe_rerun()

    if role == "student":
        st.header(f"Welcome, {user['name']} (Student)")
        tabs = st.tabs(["Request Outpass", "My Outpasses", "Attendance"])
        with tabs[0]:
            st.subheader("Request Outpass")
            reason = st.text_area("Reason")
            ft = st.time_input("From", value=time(9, 0))
            tt = st.time_input("To", value=time(17, 0))
            if st.button("Submit Outpass"):
                r = outpass_service.request_outpass(user["id"], reason, str(ft), str(tt))
                if getattr(r, "data", None):
                    st.success("Outpass requested")
                else:
                    st.error("Failed to request")
        with tabs[1]:
            st.subheader("My Outpasses")
            st.table(getattr(outpass_service.list_for_user(user["id"]), "data", []) or [])
        with tabs[2]:
            st.subheader("Attendance")
            status = st.radio("Status", ["Present", "Absent"])
            if st.button("Mark Attendance"):
                r = attendance_service.mark_attendance(user["id"], status)
                if getattr(r, "data", None):
                    st.success("Attendance marked")
                else:
                    st.error("Failed")

    elif role in ("warden", "admin"):
        st.header(f"Welcome, {user['name']} ({role.title()})")
        tabs = st.tabs(["Pending Outpasses", "Gate Logs", "Violations", "Reports", "All Outpasses"])

        with tabs[0]:
            st.subheader("Pending Outpasses")
            ops = getattr(outpass_service.list_all(), "data", []) or []
            for o in ops:
                if o.get("status") == "Pending":
                    st.markdown(f"**ID:** {o['id']} — User: {o['user_id']} — {o['reason']} ({o['from_time']} - {o['to_time']})")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button(f"Approve_{o['id']}"):
                            outpass_service.approve_outpass(o['id'])
                            safe_rerun()
                    with c2:
                        if st.button(f"Reject_{o['id']}"):
                            outpass_service.reject_outpass(o['id'])
                            safe_rerun()

        with tabs[1]:
            st.subheader("Record Gate Entry/Exit")
            uid = st.number_input("User ID", min_value=1)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Record Entry"):
                    gate_service.record_entry(uid)
                    st.success("Entry recorded")
            with c2:
                if st.button("Record Exit"):
                    gate_service.record_exit(uid)
                    st.success("Exit recorded")
            st.subheader("Recent Gate Logs")
            st.table(getattr(gate_service.get_logs(), "data", []) or [])

        with tabs[2]:
            st.subheader("Violations")
            uid = st.number_input("User ID (report)", min_value=1, key="viol_uid")
            desc = st.text_area("Description", key="viol_desc")
            if st.button("Report Violation"):
                violation_service.report_violation(uid, desc)
                st.success("Violation reported")
            st.subheader("All Violations")
            st.table(getattr(violation_service.list_violations(), "data", []) or [])

        with tabs[3]:
            st.subheader("System Reports")
            summary = report_service.system_summary()
            st.metric("Total outpasses", summary["total_outpasses"])
            st.metric("Approved", summary["approved"])
            st.metric("Pending", summary["pending"])
            st.metric("Rejected", summary["rejected"])
            st.metric("Total violations", summary["total_violations"])

        with tabs[4]:
            st.subheader("All Outpasses")
            st.table(getattr(outpass_service.list_all(), "data", []) or [])

else:
    st.info("Please register or login from the sidebar to continue.")
