import os
import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent / "database"
DB_PATH = DB_DIR / "coaching.db"


def _ensure_database():
    initialize_database()


def initialize_database():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            course TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            paid_on TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            score REAL NOT NULL,
            max_score REAL NOT NULL,
            assessed_on TEXT NOT NULL
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "admin123", "admin"))
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("student", "student123", "student"))

    conn.commit()
    conn.close()
    return str(DB_PATH)


def authenticate_user(username, password):
    if not username or not password:
        return False
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def register_user(username, password, role="student"):
    if not username or not password:
        return False
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def add_student(name, class_name, course, phone):
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, class_name, course, phone) VALUES (?, ?, ?, ?)",
        (name, class_name, course, phone),
    )
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    return student_id


def get_all_students():
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, class_name, course, phone FROM students ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_student_options():
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, class_name, course FROM students ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_student(student_id):
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()


def add_attendance(student_id, date, status):
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date, status))
    conn.commit()
    conn.close()


def get_attendance_records():
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT attendance.id, students.name, attendance.date, attendance.status
        FROM attendance
        JOIN students ON students.id = attendance.student_id
        ORDER BY attendance.date DESC, attendance.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_fee(student_id, amount, paid_on):
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fees (student_id, amount, paid_on) VALUES (?, ?, ?)", (student_id, amount, paid_on))
    conn.commit()
    conn.close()


def get_fee_records():
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT fees.id, students.name, fees.amount, fees.paid_on
        FROM fees
        JOIN students ON students.id = fees.student_id
        ORDER BY fees.paid_on DESC, fees.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_notice(title, message):
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notices (title, message) VALUES (?, ?)", (title, message))
    conn.commit()
    conn.close()


def get_notices():
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, message FROM notices ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_performance(student_id, subject, score, max_score, assessed_on):
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO performance (student_id, subject, score, max_score, assessed_on) VALUES (?, ?, ?, ?, ?)",
        (student_id, subject, score, max_score, assessed_on),
    )
    conn.commit()
    conn.close()


def get_performance():
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT performance.id, students.name, performance.subject,
               performance.score, performance.max_score, performance.assessed_on
        FROM performance
        JOIN students ON students.id = performance.student_id
        ORDER BY performance.assessed_on DESC, performance.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_dashboard_stats():
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), COUNT(DISTINCT course) FROM students")
    total_students, total_courses = cursor.fetchone()
    cursor.execute("SELECT COUNT(*), SUM(CASE WHEN LOWER(status) = 'present' THEN 1 ELSE 0 END) FROM attendance")
    attendance_total, attendance_present = cursor.fetchone()
    cursor.execute("SELECT COALESCE(SUM(amount), 0), COUNT(*) FROM fees")
    total_fees, fee_records = cursor.fetchone()
    cursor.execute("SELECT AVG(score * 100.0 / NULLIF(max_score, 0)) FROM performance")
    average_performance = cursor.fetchone()[0]
    conn.close()
    attendance_rate = (attendance_present * 100.0 / attendance_total) if attendance_total else 0
    return {
        "students": total_students,
        "courses": total_courses,
        "attendance_rate": attendance_rate,
        "fees": total_fees,
        "fee_records": fee_records,
        "average_performance": average_performance or 0,
    }
