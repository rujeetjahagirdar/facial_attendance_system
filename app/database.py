import sqlite3
import json
import os

DB_PATH = "app/facial_attendance.db"

def initialize_database():
    """Initialize SQLite database tables."""
    os.makedirs("app", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for face encodings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS face_encodings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            encoding TEXT NOT NULL
        )
    ''')

    # Table for attendance logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_face_encoding(name, encoding):
    """Insert a new face encoding into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO face_encodings (name, encoding) VALUES (?, ?)", (name, json.dumps(encoding)))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Face with name '{name}' already exists.")
    conn.close()

def fetch_face_encodings():
    """Fetch all face encodings from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, encoding FROM face_encodings")
    rows = cursor.fetchall()
    conn.close()
    return [(row[0], json.loads(row[1])) for row in rows]

def mark_attendance(name):
    """Log attendance for a recognized face."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def fetch_attendance_logs():
    """Fetch all attendance logs."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, timestamp FROM attendance")
    rows = cursor.fetchall()
    conn.close()
    return rows
