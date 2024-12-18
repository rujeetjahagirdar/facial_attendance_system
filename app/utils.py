import os
import sqlite3
import json
import face_recognition
import numpy as np

APP_DB_FILE = 'app/facial_attendance_db.db'

def db_setup():
    """Sets up the database and creates necessary tables."""
    if not os.path.exists(APP_DB_FILE):
        print("Creating facial_attendance_db...")
    with sqlite3.connect(APP_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS USERS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                encoding TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def encode_img(img_path):
    """Encodes the face in an image file."""
    if os.path.exists(img_path):
        img_data = face_recognition.load_image_file(img_path)
        img_encodings = face_recognition.face_encodings(img_data)
        if img_encodings:
            return img_encodings[0]
        print(f"Warning: No faces found in '{img_path}'.")
    else:
        print(f"Error: Image file '{img_path}' not found.")
    return None

def load_encodings():
    """Loads all encodings from the database."""
    encoding_lists = []
    try:
        with sqlite3.connect(APP_DB_FILE) as conn:
            cursor = conn.cursor()
            results = cursor.execute("SELECT id, name, encoding FROM USERS").fetchall()
            for row in results:
                encoding = np.array(json.loads(row[2]))
                encoding_lists.append((row[0], row[1], encoding))
    except Exception as e:
        print(f"Error loading encodings: {e}")
    return encoding_lists

def mark_attendance(user_name):
    """Marks attendance for a given user."""
    try:
        with sqlite3.connect(APP_DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO attendance (name) VALUES (?)", (user_name,))
            conn.commit()
            print(f"Attendance marked for {user_name}.")
    except sqlite3.Error as e:
        print(f"Error marking attendance: {e}")

def fetch_attendance_logs():
    """Fetches all attendance records."""
    try:
        with sqlite3.connect(APP_DB_FILE) as conn:
            cursor = conn.cursor()
            results = cursor.execute("SELECT name, timestamp FROM attendance").fetchall()
            return results
    except Exception as e:
        print(f"Error fetching attendance logs: {e}")
    return []
