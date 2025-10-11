import sys
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import streamlit as st
from service.auth_service import AuthService
from service.outpass_service import OutpassService
from service.attendance_service import AttendanceService
from service.gate_service import GateService
from service.violation_service import ViolationService
from service.report_service import ReportService
from datetime import time

st.set_page_config(page_title="🏫 Outpass Management System", layout="wide")
st.title("🏫 Outpass Management System")

# Initialize services
auth_service = AuthService()
outpass_service = OutpassService()
attendance_service = AttendanceService()
gate_service = GateService()
violation_service = ViolationService()
report_service = ReportService()

# ✅ Safe rerun helper for all Streamlit versions
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# Sidebar for Login/Register
st.sidebar.header("Account")
action = st.sidebar.radio("Action", ["Login", "Register"])

if action == "Register":
    name = st.sidebar.text_input("Full name")
    email = st.sidebar.text_input("Email")
    role = st.sidebar.selectbox("Role", ["student", "warden", "admin"])
    if st.sidebar.button("Register"):
        try:
            res = auth_service.register(name, email, role)
            st.sidebar.success("Registered successfully or already exists.")
        except Exception as e:
            st.sidebar.error(f"Registration failed: {e}")

elif action == "Login":
    email = st.sidebar.text_input("Email for login")
    if st.sidebar.button("Login"):
        user = auth_service.login(email)
        if user:
            st.session_state["user"] = user
            st.sidebar.success(f"Logged in as {user['name']} ({user['role']})")
        else:
            st.sidebar.error("User not found, please register first.")

# Main Page Logic
if "user" in st.session_state:
    user = st.session_state["user"]
    role = user.get("role", "student")

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.pop("user")
        safe_rerun()

    # 🎓 Student Dashboard
    if role == "student":
        st.header(f"Welcome, {user['name']} (Student)")
        tabs = st.tabs(["Request Outpass", "My Outpasses", "Attendance"])

        with tabs[0]:
            st.subheader("Request Outpass")
            reason = st.text_area("Reason")
            ft = st.time_input("From", value=time(9, 0))
            tt = st.time_input("To", value=time(17, 0))
            if st.button("Submit Outpass"):
                try:
                    r = outpass_service.request_outpass(user["id"], reason, str(ft), str(tt))
                    st.success("Outpass requested successfully.")
                except Exception as e:
                    st.error(f"Failed to request: {e}")

        with tabs[1]:
            st.subheader("My Outpasses")
            resp = outpass_service.list_for_user(user["id"])
            st.table(getattr(resp, "data", []) or [])

        with tabs[2]:
            st.subheader("Attendance")
            status = st.radio("Status", ["Present", "Absent"])
            if st.button("Mark Attendance"):
                try:
                    attendance_service.mark_attendance(user["id"], status)
                    st.success("Attendance marked successfully.")
                except Exception as e:
                    st.error(f"Failed to mark attendance: {e}")

    # 🧑‍🏫 Warden / Admin Dashboard
    elif role in ("warden", "admin"):
        st.header(f"Welcome, {user['name']} ({role.title()})")
        tabs = st.tabs(["Pending Outpasses", "Gate Logs", "Violations", "Reports", "All Outpasses"])

        # Pending outpasses
        with tabs[0]:
            st.subheader("Pending Outpasses")
            all_op = outpass_service.list_all()
            ops = getattr(all_op, "data", []) or []
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

        # Gate logs
        with tabs[1]:
            st.subheader("Record Gate Entry/Exit")
            uid = st.number_input("Enter User ID", min_value=1)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Record Entry"):
                    try:
                        gate_service.record_entry(uid)
                        st.success("Gate entry recorded.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            with c2:
                if st.button("Record Exit"):
                    try:
                        gate_service.record_exit(uid)
                        st.success("Gate exit recorded.")
                    except Exception as e:
                        st.error(f"Error: {e}")

            st.subheader("Recent Gate Logs")
            logs = gate_service.get_logs()
            st.table(getattr(logs, "data", []) or [])

        # Violations
        with tabs[2]:
            st.subheader("Report Violation")
            uid = st.number_input("User ID", min_value=1, key="viol_uid")
            desc = st.text_area("Description", key="viol_desc")
            if st.button("Report Violation"):
                try:
                    violation_service.report_violation(uid, desc)
                    st.success("Violation reported successfully.")
                except Exception as e:
                    st.error(f"Error: {e}")

            st.subheader("All Violations")
            st.table(getattr(violation_service.list_violations(), "data", []) or [])

        # Reports
        with tabs[3]:
            st.subheader("System Reports")
            summary = report_service.system_summary()
            st.metric("Total outpasses", summary["total_outpasses"])
            st.metric("Approved", summary["approved"])
            st.metric("Pending", summary["pending"])
            st.metric("Rejected", summary["rejected"])
            st.metric("Total violations", summary["total_violations"])

        # All Outpasses
        with tabs[4]:
            st.subheader("All Outpasses")
            st.table(getattr(outpass_service.list_all(), "data", []) or [])

else:
    st.info("Please register or login from the sidebar to continue.")
