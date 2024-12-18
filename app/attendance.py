import time
import cv2
import face_recognition
import numpy as np
from app.utils import load_encodings, mark_attendance
import streamlit as st


def process_video_feed():
    """Processes webcam for face recognition."""
    registered_users = load_encodings()
    users_encodings = [i[2] for i in registered_users]

    cap = cv2.VideoCapture(0)
    start_time = time.time()
    face_found = False
    placeholder = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            st.error("Error accessing webcam.")
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(users_encodings, face_encoding)

            if True in matches:
                best_match_index = np.argmin(face_recognition.face_distance(users_encodings, face_encoding))
                name = registered_users[best_match_index][1]
                mark_attendance(name)

                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                display_start_time = time.time()
                while time.time() - display_start_time < 3:

                    placeholder.image(frame, channels="BGR", use_column_width=True)

                placeholder.empty()
                cap.release()
                cv2.destroyAllWindows()
                return name

        placeholder.image(frame, channels="BGR", use_column_width=True)

        if time.time() - start_time > 10 and not face_found:
            st.error("No known face found. Closing webcam.")
            placeholder.empty()
            cap.release()
            cv2.destroyAllWindows()
            return None

    cap.release()
    cv2.destroyAllWindows()
    return None