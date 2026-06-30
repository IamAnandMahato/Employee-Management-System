import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import get_connection

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Attendance",
    page_icon="📅",
    layout="wide"
)

# ---------------------------------
# LOGIN CHECK
# ---------------------------------
if "user" not in st.session_state:
    st.error("Please login first.")
    st.stop()

# ---------------------------------
# LOAD CSS
# ---------------------------------
try:
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

conn = get_connection()
cursor = conn.cursor()

st.title("📅 Attendance Management")

# ---------------------------------
# LOAD EMPLOYEES
# ---------------------------------
employees = pd.read_sql(
    "SELECT id, name FROM employees",
    conn
)

if employees.empty:
    st.warning("No employees found.")
    st.stop()

# ---------------------------------
# MARK ATTENDANCE
# ---------------------------------
st.subheader("Mark Attendance")

col1, col2 = st.columns(2)

with col1:

    employee = st.selectbox(
        "Employee",
        employees["name"]
    )

    employee_id = employees.loc[
        employees["name"] == employee,
        "id"
    ].values[0]

with col2:

    status = st.selectbox(
        "Status",
        [
            "Present",
            "Absent",
            "Work From Home"
        ]
    )

checkin = datetime.now().strftime("%H:%M:%S")

if st.button(
    "Mark Attendance",
    use_container_width=True
):

    cursor.execute(
        """
        INSERT INTO attendance
        (
            employee_id,
            date,
            status,
            check_in,
            check_out
        )
        VALUES(?,?,?,?,?)
        """,
        (
            int(employee_id),
            str(date.today()),
            status,
            checkin,
            ""
        )
    )

    conn.commit()

    st.success("Attendance Recorded Successfully")

    st.rerun()

st.divider()

# ---------------------------------
# TODAY'S ATTENDANCE
# ---------------------------------
st.subheader("Today's Attendance")

attendance = pd.read_sql(
    """
    SELECT

    attendance.id,
    employees.name,
    attendance.date,
    attendance.status,
    attendance.check_in,
    attendance.check_out

    FROM attendance

    INNER JOIN employees

    ON attendance.employee_id = employees.id

    ORDER BY attendance.date DESC

    """,
    conn
)

search = st.text_input(
    "🔍 Search Employee"
)

if search:

    attendance = attendance[
        attendance["name"].str.contains(
            search,
            case=False
        )
    ]

st.dataframe(
    attendance,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "📥 Download Attendance",
    attendance.to_csv(index=False),
    "attendance.csv",
    "text/csv",
    use_container_width=True
)

# ---------------------------------
# SUMMARY
# ---------------------------------
st.divider()

st.subheader("Attendance Summary")

c1, c2, c3 = st.columns(3)

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

wfh = len(
    attendance[
        attendance["status"] == "Work From Home"
    ]
)

c1.metric("Present", present)
c2.metric("Absent", absent)
c3.metric("Work From Home", wfh)

conn.close()
