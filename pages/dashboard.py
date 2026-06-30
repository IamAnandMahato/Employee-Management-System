import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from auth import logout_user

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOGIN CHECK
# -----------------------------
if "user" not in st.session_state:
    st.error("Please login first.")
    st.stop()

user = st.session_state["user"]

# -----------------------------
# LOAD CSS
# -----------------------------
try:
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

# -----------------------------
# DATABASE
# -----------------------------
conn = sqlite3.connect(
    "database/employee.db",
    check_same_thread=False
)

employees = pd.read_sql(
    "SELECT * FROM employees",
    conn
)

attendance = pd.read_sql(
    "SELECT * FROM attendance",
    conn
)

leaves = pd.read_sql(
    "SELECT * FROM leaves",
    conn
)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("💼 EMS")

    st.success(f"Welcome\n\n**{user['name']}**")

    st.page_link(
        "pages/dashboard.py",
        label="Dashboard",
        icon="🏠"
    )

    st.page_link(
        "pages/employees.py",
        label="Employees",
        icon="👨‍💼"
    )

    st.page_link(
        "pages/attendance.py",
        label="Attendance",
        icon="📅"
    )

    st.page_link(
        "pages/leave.py",
        label="Leave",
        icon="📝"
    )

    st.page_link(
        "pages/reports.py",
        label="Reports",
        icon="📊"
    )

    st.page_link(
        "pages/profile.py",
        label="Profile",
        icon="👤"
    )

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        logout_user(st)
        st.switch_page("app.py")

# -----------------------------
# HEADER
# -----------------------------
st.title("📊 Dashboard")

st.caption("Employee Management System")

# -----------------------------
# METRICS
# -----------------------------
total_emp = len(employees)

present = len(
    attendance[
        attendance["status"] == "Present"
    ]
)

pending_leave = len(
    leaves[
        leaves["status"] == "Pending"
    ]
)

departments = employees["department"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Employees", total_emp)

c2.metric("Present", present)

c3.metric("Pending Leave", pending_leave)

c4.metric("Departments", departments)

st.divider()

# -----------------------------
# CHARTS
# -----------------------------
left, right = st.columns(2)

with left:

    if len(employees):

        dept = employees.groupby(
            "department"
        ).size().reset_index(name="Employees")

        fig = px.bar(
            dept,
            x="department",
            y="Employees",
            text="Employees",
            title="Employees by Department"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with right:

    if len(attendance):

        status = attendance.groupby(
            "status"
        ).size().reset_index(name="Count")

        fig = px.pie(
            status,
            values="Count",
            names="status",
            hole=.5,
            title="Attendance Summary"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# -----------------------------
# TABLES
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("👨 Recent Employees")

    if len(employees):

        st.dataframe(
            employees.tail(5),
            use_container_width=True,
            hide_index=True
        )
    else:

        st.info("No Employees Found")

with col2:

    st.subheader("📝 Pending Leaves")

    if len(leaves):

        pending = leaves[
            leaves["status"] == "Pending"
        ]

        st.dataframe(
            pending,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("No Pending Leaves")

st.divider()

# -----------------------------
# FOOTER
# -----------------------------
st.caption("Employee Management System | Python • Streamlit • SQLite")