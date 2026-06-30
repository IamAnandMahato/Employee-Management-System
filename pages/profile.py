import streamlit as st
import pandas as pd
from database import get_connection

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="My Profile",
    page_icon="👤",
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

user = st.session_state["user"]

conn = get_connection()

employee = pd.read_sql(
    "SELECT * FROM employees WHERE id=?",
    conn,
    params=(user["id"],)
)

conn.close()

if employee.empty:
    st.error("Employee not found.")
    st.stop()

employee = employee.iloc[0]

# ---------------------------------------
# HEADER
# ---------------------------------------

st.title("👤 My Profile")

st.markdown("---")

col1, col2 = st.columns([1,3])

# ---------------------------------------
# PROFILE IMAGE
# ---------------------------------------

with col1:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=180
    )

# ---------------------------------------
# PROFILE DETAILS
# ---------------------------------------

with col2:

    st.subheader(employee["name"])

    st.write(f"**Role:** {employee['role']}")
    st.write(f"**Department:** {employee['department']}")
    st.write(f"**Designation:** {employee['designation']}")
    st.write(f"**Email:** {employee['email']}")
    st.write(f"**Phone:** {employee['phone']}")
    st.write(f"**Joining Date:** {employee['joining_date']}")

    if user["role"] == "Admin":
        st.write(f"**Salary:** ₹ {employee['salary']}")

st.markdown("---")

# ---------------------------------------
# PROFILE SUMMARY
# ---------------------------------------

st.subheader("Profile Summary")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Department",
    employee["department"]
)

c2.metric(
    "Designation",
    employee["designation"]
)

c3.metric(
    "Role",
    employee["role"]
)

st.markdown("---")

# ---------------------------------------
# EDIT PROFILE
# ---------------------------------------

st.subheader("Update Contact Information")

new_phone = st.text_input(
    "Phone Number",
    employee["phone"]
)

if st.button("Update Profile"):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE employees
        SET phone=?
        WHERE id=?
        """,
        (
            new_phone,
            employee["id"]
        )
    )

    conn.commit()

    conn.close()

    st.success("Profile Updated Successfully!")
    st.rerun()