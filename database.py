import sqlite3
import os

DATABASE_PATH = "database/employee.db"


def get_connection():
    """
    Create database connection.
    """
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


def create_tables():
    """
    Create all required tables.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Employee Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        department TEXT,

        designation TEXT,

        salary REAL,

        phone TEXT,

        role TEXT DEFAULT 'Employee',

        joining_date TEXT

    )
    """)

    # Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id INTEGER,

        date TEXT,

        status TEXT,

        check_in TEXT,

        check_out TEXT,

        FOREIGN KEY(employee_id)
        REFERENCES employees(id)

    )
    """)

    # Leave Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leaves(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id INTEGER,

        leave_type TEXT,

        from_date TEXT,

        to_date TEXT,

        reason TEXT,

        status TEXT DEFAULT 'Pending',

        FOREIGN KEY(employee_id)
        REFERENCES employees(id)

    )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# Employee Functions
# ----------------------------

def get_all_employees():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_employee_by_email(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM employees WHERE email=?",
        (email,)
    )

    row = cursor.fetchone()

    conn.close()

    return row


def add_employee(
    name,
    email,
    password,
    department,
    designation,
    salary,
    phone,
    role,
    joining_date
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO employees

    (
    name,
    email,
    password,
    department,
    designation,
    salary,
    phone,
    role,
    joining_date
    )

    VALUES(?,?,?,?,?,?,?,?,?)

    """,

    (
        name,
        email,
        password,
        department,
        designation,
        salary,
        phone,
        role,
        joining_date
    )
    )

    conn.commit()

    conn.close()


def update_employee(
    emp_id,
    name,
    department,
    designation,
    salary,
    phone
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE employees

    SET

    name=?,
    department=?,
    designation=?,
    salary=?,
    phone=?

    WHERE id=?

    """,

    (
        name,
        department,
        designation,
        salary,
        phone,
        emp_id
    )
    )

    conn.commit()

    conn.close()


def delete_employee(emp_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=?",
        (emp_id,)
    )

    conn.commit()

    conn.close()


# ----------------------------
# Attendance
# ----------------------------

def mark_attendance(
    employee_id,
    date,
    status,
    check_in,
    check_out
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

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
        employee_id,
        date,
        status,
        check_in,
        check_out
    )
    )

    conn.commit()

    conn.close()


# ----------------------------
# Leave
# ----------------------------

def apply_leave(
    employee_id,
    leave_type,
    from_date,
    to_date,
    reason
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

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
        employee_id,
        leave_type,
        from_date,
        to_date,
        reason,
        "Pending"
    )
    )

    conn.commit()

    conn.close()


# ----------------------------
# Initialize Database
# ----------------------------

if __name__ == "__main__":
    create_tables()
    print("Database Created Successfully")