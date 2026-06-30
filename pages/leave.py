import streamlit as st
import pandas as pd
from database import get_connection

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------
st.set_page_config(
    page_title="Leave Management",
    page_icon="📝",
    layout="wide"
)

# ----------------------------------------
# LOGIN CHECK
# ----------------------------------------
if "user" not in st.session_state:
    st.error("Please login first.")
    st.stop()

user = st.session_state["user"]

# ----------------------------------------
# LOAD CSS
# ----------------------------------------
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

st.title("📝 Leave Management")

# ========================================
# APPLY LEAVE
# ========================================

with st.expander("Apply Leave", expanded=True):

    employees = pd.read_sql(
        "SELECT id,name FROM employees",
        conn
    )

    employee = st.selectbox(
        "Employee",
        employees["name"]
    )

    employee_id = employees.loc[
        employees["name"] == employee,
        "id"
    ].values[0]

    leave_type = st.selectbox(
        "Leave Type",
        [
            "Casual Leave",
            "Sick Leave",
            "Annual Leave",
            "Emergency Leave"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        from_date = st.date_input("From Date")

    with col2:
        to_date = st.date_input("To Date")

    reason = st.text_area("Reason")

    if st.button(
        "Submit Leave Request",
        use_container_width=True
    ):

        cursor.execute(
            """
            INSERT INTO leaves
            (
                employee_id,
                leave_type,
                from_date,
                to_date,
                reason,
                status
            )

            VALUES(?,?,?,?,?,?)
            """,
            (
                int(employee_id),
                leave_type,
                str(from_date),
                str(to_date),
                reason,
                "Pending"
            )
        )

        conn.commit()

        st.success("Leave Request Submitted")

        st.rerun()

# ========================================
# LEAVE REQUESTS
# ========================================

st.divider()

st.subheader("Leave Requests")

query = """

SELECT

leaves.id,

employees.name,

leave_type,

from_date,

to_date,

reason,

status

FROM leaves

INNER JOIN employees

ON employees.id = leaves.employee_id

ORDER BY leaves.id DESC

"""

df = pd.read_sql(query, conn)

search = st.text_input("Search Employee")

if search:

    df = df[
        df["name"].str.contains(
            search,
            case=False
        )
    ]

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ========================================
# ADMIN APPROVAL
# ========================================

if user["role"] == "Admin":

    st.divider()

    st.subheader("Approve / Reject Leave")

    pending = pd.read_sql(
        """
        SELECT

        leaves.id,

        employees.name,

        leave_type,

        status

        FROM leaves

        INNER JOIN employees

        ON employees.id=leaves.employee_id

        WHERE status='Pending'
        """,
        conn
    )

    if len(pending):

        leave_id = st.selectbox(
            "Pending Leave ID",
            pending["id"]
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Approve",
                use_container_width=True
            ):

                cursor.execute(
                    """
                    UPDATE leaves

                    SET status='Approved'

                    WHERE id=?
                    """,
                    (int(leave_id),)
                )

                conn.commit()

                st.success("Leave Approved")

                st.rerun()

        with col2:

            if st.button(
                "Reject",
                use_container_width=True
            ):

                cursor.execute(
                    """
                    UPDATE leaves

                    SET status='Rejected'

                    WHERE id=?
                    """,
                    (int(leave_id),)
                )

                conn.commit()

                st.success("Leave Rejected")

                st.rerun()

    else:

        st.success("No Pending Leave Requests")

# ========================================
# DASHBOARD
# ========================================

st.divider()

st.subheader("Leave Summary")

approved = len(df[df["status"] == "Approved"])

pending = len(df[df["status"] == "Pending"])

rejected = len(df[df["status"] == "Rejected"])

c1, c2, c3 = st.columns(3)

c1.metric("Approved", approved)

c2.metric("Pending", pending)

c3.metric("Rejected", rejected)

# ========================================
# DOWNLOAD
# ========================================

st.download_button(
    "📥 Download Leave Report",
    df.to_csv(index=False),
    "leave_report.csv",
    "text/csv",
    use_container_width=True
)

conn.close()