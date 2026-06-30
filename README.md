# 👨‍💼 Employee Management System

A professional **Employee Management System (EMS)** built using **Python, Streamlit, SQLite, Pandas, Plotly, and bcrypt**. The application enables organizations to efficiently manage employees, attendance, leave requests, and reports through an intuitive web interface.

---

## 🚀 Features

### 🔐 Authentication
- Secure login with bcrypt password hashing
- Role-based access (Admin & Employee)
- Session management
- Logout functionality

### 👨‍💼 Employee Management
- Add Employee
- Update Employee
- Delete Employee
- Search Employee
- Employee List
- Download Employee Data (CSV)

### 📅 Attendance Management
- Mark Attendance
- View Attendance History
- Search Attendance
- Attendance Summary
- Export Attendance Report

### 📝 Leave Management
- Apply Leave
- Approve / Reject Leave (Admin)
- Leave History
- Leave Dashboard
- Export Leave Report

### 📊 Dashboard
- Total Employees
- Present Employees
- Pending Leave Requests
- Department Count
- Interactive Charts
- Recent Employees
- Pending Leave Requests

### 📈 Reports
- Employee Analytics
- Attendance Analytics
- Leave Analytics
- Interactive Plotly Charts
- CSV Export

### 👤 Profile
- Employee Details
- Update Contact Number
- Salary Visibility (Admin)
- Department & Designation Information

---

# 🛠️ Tech Stack

- Python 3.x
- Streamlit
- SQLite
- Pandas
- Plotly
- bcrypt

---

# 📁 Project Structure

```text
Employee-Management-System/

│
├── app.py
├── auth.py
├── database.py
├── create_admin.py
├── requirements.txt
├── README.md
│
├── assets/
│     style.css
│
├── database/
│     employee.db
│
├── pages/
│     dashboard.py
│     employees.py
│     attendance.py
│     leave.py
│     reports.py
│     profile.py
│
└── .streamlit/
      config.toml
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/employee-management-system-streamlit.git
```

## 2. Navigate to Project

```bash
cd employee-management-system-streamlit
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Create the Database & Admin Account

```bash
python create_admin.py
```

## 5. Run the Application

```bash
streamlit run app.py
```

---

# 🔑 Default Admin Login

| Email | Password |
|--------|----------|
| admin@gmail.com | admin123 |

> Change the default password after your first login if you plan to use the application beyond development.

---

# 📸 Screenshots

You can add screenshots here after running the project.

- Login Page
- Dashboard
- Employee Management
- Attendance
- Leave Management
- Reports
- Profile

---

# 🎯 Future Enhancements

- Employee Photo Upload
- Email Notifications
- Forgot Password
- PDF Report Export
- Holiday Calendar
- Payroll Module
- Multi-Company Support
- REST API
- Docker Support
- Cloud Database Integration

---

# 👨‍💻 Author

**Sachin**

---

# 📄 License

This project is released under the MIT License.
