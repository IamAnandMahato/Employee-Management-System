import bcrypt
from database import get_employee_by_email


# ----------------------------
# Password Hashing
# ----------------------------

def hash_password(password):
    """
    Convert plain password into hashed password.
    """
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


# ----------------------------
# Verify Password
# ----------------------------

def verify_password(password, hashed_password):
    """
    Verify entered password.
    """

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ----------------------------
# Login
# ----------------------------

def login(email, password):

    employee = get_employee_by_email(email)

    if employee is None:
        return None

    if verify_password(password, employee["password"]):
        return employee

    return None


# ----------------------------
# Role Check
# ----------------------------

def is_admin(user):

    if user is None:
        return False

    return user["role"] == "Admin"


# ----------------------------
# Session Functions
# ----------------------------

def login_user(st, user):
    """
    Save logged-in user in session.
    """

    st.session_state["user"] = dict(user)


def logout_user(st):
    """
    Clear user session.
    """

    if "user" in st.session_state:
        del st.session_state["user"]


def is_logged_in(st):
    """
    Check whether user is logged in.
    """

    return "user" in st.session_state