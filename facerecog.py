import os
import cv2
import shutil
import numpy as np
import face_recognition
import customtkinter as ctk
from datetime import datetime
import threading
from tkinter import filedialog
import subprocess  
from sound import playsound2,Playsound1
import time
# -------------------- Setup -------------------- #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Image folder setup
path = 'images path'
if not os.path.exists(path):
    os.makedirs(path)

images = []
ClassName = []
mylist = os.listdir(path)

for cl in mylist:
    curimg = cv2.imread(f'{path}/{cl}')
    if curimg is not None:
        images.append(curimg)
        ClassName.append(os.path.splitext(cl)[0])

def FindEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encodeList.append(encodes[0])
    return encodeList

def markAttendance(name):
    with open('attendance.csv', 'a+') as f:
        f.seek(0)
        mydatalist = f.readlines()
        namelist = [line.split(',')[0] for line in mydatalist]
        if name not in namelist:
            now = datetime.now()
            datestring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{datestring}')
            print(f"✅ Marked: {name} at {datestring}")

encodeListKnown = FindEncoding(images)
print("Encoding Complete ✅")

# -------------------- Detection Function -------------------- #
friendly_faces = ['roshan panda', 'Sunil reddy-vikash', 'roshan']  # Add friendly face names
triggered_friendly_faces = set()

def start_detection(camera_index):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"❌ Could not open camera {camera_index}")
        return

    while True:
        success, img = cap.read()
        if not success:
            break

        imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgs)
        encodesCurFrame = face_recognition.face_encodings(imgs, faceCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = ClassName[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 255, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)

                threading.Thread(target=markAttendance, args=(name,), daemon=True).start()

                # 🚨 Friendly face detected, run main.py once
                if name.lower() in [f.lower() for f in friendly_faces] and name not in triggered_friendly_faces:
                    triggered_friendly_faces.add(name)
                    print(f"🤝 Friendly face {name} detected! Launching main.py...")
                    threading.Thread(target=lambda: subprocess.Popen(["python", "main.py"]), daemon=True).start()
                    playsound2()
                    cap.release()
                    cv2.destroyAllWindows()
                else:
                    Playsound1()

        cv2.imshow(f'Face Recognition - Camera {camera_index}', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# -------------------- Upload Face Image -------------------- #
def upload_image():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        dest_path = os.path.join(path, filename)
        shutil.copy(file_path, dest_path)
        print(f"📷 Uploaded: {filename}")
    # Refresh encodings after upload
    refresh_encodings()

def refresh_encodings():
    global images, ClassName, encodeListKnown
    images = []
    ClassName = []
    mylist = os.listdir(path)
    for cl in mylist:
        curimg = cv2.imread(f'{path}/{cl}')
        if curimg is not None:
            images.append(curimg)
            ClassName.append(os.path.splitext(cl)[0])
    encodeListKnown = FindEncoding(images)
    print("🔁 Encodings updated after upload.")

# -------------------- GUI Setup -------------------- #
app = ctk.CTk()
app.geometry("400x500")
app.title("Face Recognition System")

label = ctk.CTkLabel(app, text="Face Recognition security", font=("Arial", 20))
label.pack(pady=20)

upload_btn = ctk.CTkButton(app, text="Upload Face Image", command=upload_image)
upload_btn.pack(pady=10)

# Camera buttons
def handle_camera(index):
    threading.Thread(target=start_detection, args=(index,), daemon=True).start()

btn1 = ctk.CTkButton(app, text="Start Detecting (Cam 0)", command=lambda: handle_camera(0))
btn1.pack(pady=10)

btn2 = ctk.CTkButton(app, text="Start Detecting (Cam 1)", command=lambda: handle_camera(1))
btn2.pack(pady=10)

btn3 = ctk.CTkButton(app, text="Start Detecting (Cam 2)", command=lambda: handle_camera(2))
btn3.pack(pady=10)

app.mainloop()
