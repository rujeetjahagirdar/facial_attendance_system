import json
import os
import sqlite3
from app.utils import encode_img


IMAGES_DIR = 'app/images/'
APP_DB_FILE = 'app/facial_attendance_db.db'

os.makedirs(IMAGES_DIR, exist_ok=True)

def register_user(user_image_path, user_name):
    if not os.path.exists(user_image_path):
        print(f"Error: Image path '{user_image_path}' does not exist.")
        return False


    encoded_img_data = encode_img(user_image_path)
    if encoded_img_data is None:
        print("Error: No encodings found in the provided image.")
        return False

    try:

        with sqlite3.connect(APP_DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, encoding) VALUES (?, ?)",
                (user_name, json.dumps(encoded_img_data.tolist()))
            )
            conn.commit()
            print(f"User '{user_name}' registered successfully.")
            return True
    except sqlite3.IntegrityError:
        print(f"Error: User with the name '{user_name}' already exists.")
    except Exception as e:
        print(f"Error: Unable to register user '{user_name}'. Details: {e}")
    return False