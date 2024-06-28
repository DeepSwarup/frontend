from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import face_recognition
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Directory containing known face images
known_faces_dir = 'C:/Users/deeps/Documents/python/project/assets'

# Load known faces
known_faces = []
known_names = []
for filename in os.listdir(known_faces_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image = face_recognition.load_image_file(f"{known_faces_dir}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(filename.split('.')[0])

# Function to recognize face
def recognize_face(captured_image):
    face_encodings = face_recognition.face_encodings(captured_image)
    if len(face_encodings) == 0:
        return None
    captured_encoding = face_encodings[0]
    matches = face_recognition.compare_faces(known_faces, captured_encoding)
    if True in matches:
        first_match_index = matches.index(True)
        return known_names[first_match_index]
    return None

# Function to check if attendance is already marked for today
def is_attendance_marked(student_name, file='attendance.xlsx'):
    try:
        df = pd.read_excel(file)
        today = datetime.now().strftime("%Y-%m-%d")
        return not df[(df['Name'] == student_name) & (df['Date'] == today)].empty
    except FileNotFoundError:
        return False

# Function to mark attendance
def mark_attendance(student_name, file='attendance.xlsx'):
    if is_attendance_marked(student_name, file):
        return False  # Attendance already marked today
    else:
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        try:
            df = pd.read_excel(file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Name", "Date", "Time"])
        new_record_df = pd.DataFrame({"Name": [student_name], "Date": [current_date], "Time": [current_time]})
        df = pd.concat([df, new_record_df], ignore_index=True)
        df.to_excel(file, index=False)
        return True  # Attendance marked successfully

@app.route('/recognize', methods=['POST'])
def recognize():
    files = request.files.getlist('images')
    if not files:
        return jsonify({"error": "No images provided"}), 400

    frames = []
    for file in files:
        file.save('captured_image.jpg')
        image = face_recognition.load_image_file('captured_image.jpg')
        frames.append(image)

    student_name = recognize_face(frames[0])
    if student_name is None:
        return jsonify({"error": "Student not recognized!"}), 400

    if is_attendance_marked(student_name):
        return jsonify({"message": "Your attendance is already marked for today."}), 200

    if mark_attendance(student_name):
        return jsonify({"message": f"Attendance marked for {student_name}"}), 200
    else:
        return jsonify({"error": "Failed to mark attendance."}), 500
    

@app.route('/recent-attendance', methods=['GET'])
def recent_attendance():
    try:
        df = pd.read_excel('attendance.xlsx')  # Load attendance data from Excel
        recent_entries = df.tail(15).to_dict('records')  # Get recent 15 entries as list of dicts
        return jsonify(recent_entries), 200
    except FileNotFoundError:
        return jsonify([]), 404  # Return empty list if file not found
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle other exceptions


if __name__ == '__main__':
    app.run(debug=True)
