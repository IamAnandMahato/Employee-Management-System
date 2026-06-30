from datetime import datetime
from database import create_tables, get_connection
from auth import hash_password


def create_admin():

    create_tables()

    conn = get_connection()
    cursor = conn.cursor()

    # Check if admin already exists
    cursor.execute(
        "SELECT * FROM employees WHERE email=?",
        ("admin@gmail.com",)
    )

    admin = cursor.fetchone()

    if admin:
        print("✅ Admin already exists.")
        conn.close()
        return

    cursor.execute(
        """
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

        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "System Administrator",
            "admin@gmail.com",
            hash_password("admin123"),
            "Administration",
            "Administrator",
            75000,
            "9999999999",
            "Admin",
            datetime.today().strftime("%Y-%m-%d")
        )
    )

    conn.commit()
    conn.close()

    print("--------------------------------")
    print("Admin Created Successfully")
    print("--------------------------------")
    print("Email    : admin@gmail.com")
    print("Password : admin123")
    print("--------------------------------")


if __name__ == "__main__":
    create_admin()