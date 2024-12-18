import os
import streamlit as st
from app.utils import db_setup, fetch_attendance_logs
from app.registration import register_user
from app.attendance import process_video_feed
import re

IMG_FOLDER = 'app/images'
db_setup()

st.title("Facial Attendance System")
menu = st.sidebar.selectbox("Choose an option", ["Register Face", "Mark Attendance", "View Attendance"])

def sanitize_filename(name):
    """Sanitize user input to create safe file names."""
    return re.sub(r'[^\w\s]', '', name).replace(" ", "_")

if menu == 'Register Face':
    st.subheader("Register New User")
    uploaded_img = st.file_uploader("Upload user image", type=["jpg", "jpeg", "png"])
    user_name = st.text_input("Enter User's Name: ")
    btn = st.button("Register User")
    if uploaded_img and user_name and btn:
        sanitized_name = sanitize_filename(user_name)
        img_path = os.path.join(IMG_FOLDER, f"{sanitized_name}.jpg")
        os.makedirs(IMG_FOLDER, exist_ok=True)

        with open(img_path, "wb") as f:
            f.write(uploaded_img.getbuffer())

        if register_user(img_path, sanitized_name):
            st.success(f"User '{sanitized_name}' registered successfully.")
        else:
            st.error(f"Could not register user '{sanitized_name}'.")

elif menu == 'Mark Attendance':
    st.subheader("Mark Attendance")
    st.info("Press 'Mark Attendance' to start the webcam. Ensure your face is visible.")

    if st.button("Mark Attendance"):
        user_name = process_video_feed()
        if user_name:
            st.success(f"Attendance marked for '{user_name}'.")
        else:
            st.error("No known face detected. Attendance not marked.")

elif menu == 'View Attendance':
    st.subheader("View Attendance")
    logs = fetch_attendance_logs()
    if logs:
        st.table(logs)
    else:
        st.info("No attendance records found.")
