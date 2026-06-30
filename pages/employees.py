import streamlit as st
import pandas as pd
from datetime import date
from auth import hash_password
from database import (
    get_connection,
    add_employee,
    update_employee,
    delete_employee
)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Employees",
    page_icon="👨‍💼",
    layout="wide"
)

# -----------------------------
# LOGIN CHECK
# -----------------------------
if "user" not in st.session_state:
    st.error("Please login first.")
    st.stop()

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
conn = get_connection()

# -----------------------------
# TITLE
# -----------------------------
st.title("👨‍💼 Employee Management")

tab1, tab2, tab3 = st.tabs(
    [
        "📋 Employee List",
        "➕ Add Employee",
        "✏ Update Employee"
    ]
)

# =====================================================
# EMPLOYEE LIST
# =====================================================

with tab1:

    employees = pd.read_sql(
        "SELECT * FROM employees",
        conn
    )

    search = st.text_input(
        "🔍 Search Employee"
    )

    if search:

        employees = employees[
            employees["name"].str.contains(
                search,
                case=False
            )
        ]

    st.dataframe(
        employees,
        use_container_width=True,
        hide_index=True
    )

    csv = employees.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download CSV",
        csv,
        "employees.csv",
        "text/csv"
    )

# =====================================================
# ADD EMPLOYEE
# =====================================================

with tab2:

    st.subheader("Add New Employee")

    c1, c2 = st.columns(2)

    with c1:

        name = st.text_input("Name")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        phone = st.text_input("Phone")

    with c2:

        department = st.selectbox(
            "Department",
            [
                "HR",
                "IT",
                "Finance",
                "Sales",
                "Marketing"
            ]
        )

        designation = st.text_input(
            "Designation"
        )

        salary = st.number_input(
            "Salary",
            min_value=0
        )

        role = st.selectbox(
            "Role",
            [
                "Employee",
                "Admin"
            ]
        )

    if st.button(
        "Add Employee",
        use_container_width=True
    ):

        if name == "" or email == "" or password == "":

            st.warning(
                "Please fill all required fields."
            )

        else:

            add_employee(

                name,

                email,

                hash_password(password),

                department,

                designation,

                salary,

                phone,

                role,

                str(date.today())

            )

            st.success(
                "Employee Added Successfully"
            )

            st.rerun()

# =====================================================
# UPDATE / DELETE
# =====================================================

with tab3:

    employees = pd.read_sql(
        "SELECT * FROM employees",
        conn
    )

    ids = employees["id"].tolist()

    if len(ids) == 0:

        st.info("No Employees Found.")

    else:

        emp_id = st.selectbox(
            "Select Employee",
            ids
        )

        emp = employees[
            employees["id"] == emp_id
        ].iloc[0]

        name = st.text_input(
            "Name",
            emp["name"]
        )

        department = st.text_input(
            "Department",
            emp["department"]
        )

        designation = st.text_input(
            "Designation",
            emp["designation"]
        )

        salary = st.number_input(
            "Salary",
            value=float(emp["salary"])
        )

        phone = st.text_input(
            "Phone",
            emp["phone"]
        )

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "Update Employee",
                use_container_width=True
            ):

                update_employee(

                    emp_id,

                    name,

                    department,

                    designation,

                    salary,

                    phone

                )

                st.success(
                    "Employee Updated Successfully"
                )

                st.rerun()

        with c2:

            if st.button(
                "Delete Employee",
                use_container_width=True,
                type="primary"
            ):

                delete_employee(emp_id)

                st.success(
                    "Employee Deleted Successfully"
                )

                st.rerun()

conn.close()