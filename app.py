import streamlit as st
from database import create_tables
from auth import login, login_user, is_logged_in

# -----------------------------
# Initial Setup
# -----------------------------
st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="centered"
)

create_tables()

# -----------------------------
# Redirect if already logged in
# -----------------------------
if is_logged_in(st):
    st.switch_page("pages/dashboard.py")

# -----------------------------
# Load CSS
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
# Login UI
# -----------------------------
st.markdown(
    """
    <h1 style='text-align:center;color:#2563EB'>
        Employee Management System
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("### Login")

email = st.text_input(
    "Email Address",
    placeholder="Enter your email"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter your password"
)

remember = st.checkbox("Remember Me")

if st.button("Login", use_container_width=True):

    if email == "" or password == "":
        st.warning("Please enter Email and Password.")
        st.stop()

    user = login(email, password)

    if user:

        login_user(st, user)

        st.success(f"Welcome {user['name']}!")

        st.balloons()

        st.switch_page("pages/dashboard.py")

    else:

        st.error("Invalid Email or Password")

st.divider()

st.info(
"""
Default Admin Login

Email:
admin@gmail.com

Password:
admin123
"""
)