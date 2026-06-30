import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="Reports",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------
# LOGIN CHECK
# ---------------------------------------

if "user" not in st.session_state:
    st.error("Please login first.")
    st.stop()

# ---------------------------------------
# LOAD CSS
# ---------------------------------------

try:
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

# ---------------------------------------
# DATABASE
# ---------------------------------------

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

st.title("📈 Reports & Analytics")

# ---------------------------------------
# KPI CARDS
# ---------------------------------------

total_emp = len(employees)

present = len(
    attendance[
        attendance["status"] == "Present"
    ]
)

absent = len(
    attendance[
        attendance["status"] == "Absent"
    ]
)

pending_leave = len(
    leaves[
        leaves["status"] == "Pending"
    ]
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Employees", total_emp)
c2.metric("Present", present)
c3.metric("Absent", absent)
c4.metric("Pending Leave", pending_leave)

st.divider()

# ---------------------------------------
# CHARTS
# ---------------------------------------

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
            color="department",
            text="Employees",
            title="Department Wise Employees"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with right:

    if len(attendance):

        att = attendance.groupby(
            "status"
        ).size().reset_index(name="Count")

        fig = px.pie(
            att,
            names="status",
            values="Count",
            hole=.4,
            title="Attendance Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# ---------------------------------------
# LEAVE CHART
# ---------------------------------------

if len(leaves):

    leave_chart = leaves.groupby(
        "status"
    ).size().reset_index(name="Count")

    fig = px.bar(
        leave_chart,
        x="status",
        y="Count",
        color="status",
        text="Count",
        title="Leave Requests"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ---------------------------------------
# EMPLOYEE TABLE
# ---------------------------------------

st.subheader("Employee Report")

st.dataframe(
    employees,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "⬇ Download Employee Report",
    employees.to_csv(index=False),
    "employees.csv",
    "text/csv",
    use_container_width=True
)

st.divider()

# ---------------------------------------
# ATTENDANCE TABLE
# ---------------------------------------

st.subheader("Attendance Report")

attendance_report = pd.read_sql("""

SELECT

employees.name,

attendance.date,

attendance.status,

attendance.check_in,

attendance.check_out

FROM attendance

INNER JOIN employees

ON employees.id = attendance.employee_id

""", conn)

st.dataframe(
    attendance_report,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "⬇ Download Attendance Report",
    attendance_report.to_csv(index=False),
    "attendance.csv",
    "text/csv",
    use_container_width=True
)

st.divider()

# ---------------------------------------
# LEAVE REPORT
# ---------------------------------------

st.subheader("Leave Report")

leave_report = pd.read_sql("""

SELECT

employees.name,

leave_type,

from_date,

to_date,

status

FROM leaves

INNER JOIN employees

ON employees.id = leaves.employee_id

""", conn)

st.dataframe(
    leave_report,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "⬇ Download Leave Report",
    leave_report.to_csv(index=False),
    "leave_report.csv",
    "text/csv",
    use_container_width=True
)

conn.close()