import cv2
import threading
import customtkinter as ctk
from sound import Playsound1, playsound2  # Defined in sound.py
from datetime import datetime
import subprocess
from sendmessage import send_intruder_alert
from dblogger import push_latest_log
import os
import json
def log_detection_data(sound_name, cam_index):
    now = datetime.now().strftime("%H:%M:%S")

    # Load the saved phone number (if available)
    try:
        with open("numbers.txt", "r") as number_file:
            phone_number = number_file.readline().strip()
    except FileNotFoundError:
        phone_number = "Not available"

    # Prepare log dictionary
    log_data = {
        "alarm": sound_name,
        "face_detection": True,
        "detection": "intruder",
        "camera": cam_index,
        "number": phone_number,
        "time":now
    }

    # Write as a JSON line to log.txt
    with open("log.txt", "a") as file:
        file.write(json.dumps(log_data) + "\n")

    print("[Logger] Log written:", log_data)
# Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Globals
sound_played = False
cap = None
selected_sound = None  # Will be a function reference

# --- Face Detection ---
def start_detection():
    global sound_played, cap, selected_sound

    cam_index = int(camera_entry.get())
    cap = cv2.VideoCapture(cam_index)

    def detection():
        global sound_played

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # after face got detected
            if len(faces) > 0 and not sound_played:
                sound_played = True
                if selected_sound is not None:
                    threading.Thread(target=selected_sound, daemon=True).start()
                    log_detection_data(
                        sound_name=selected_sound.__name__,
                        cam_index=cam_index
                    )
                threading.Thread(target=send_intruder_alert, daemon=True).start()
                threading.Thread(target=push_latest_log, daemon=True).start()

            elif len(faces) == 0:
                sound_played = False

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)

            cv2.putText(frame, "Press Q to exit", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.imshow("Face Detection with Sound", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=detection, daemon=True).start()

def text_config():
    subprocess.Popen(["python", "textsetting.py"])

def admin_config():
    subprocess.Popen(["python", "admin_pwdchange.py"])

def logfun():
    subprocess.Popen(["notepad.exe", "log.txt"])

def seeadmin():
    subprocess.Popen(["notepad.exe","admin-details.txt"])

def textfun():
    subprocess.Popen(["notepad.exe", "numbers.txt"])

# --- Sound Selection Buttons ---
def play_sound1():
    global selected_sound
    selected_sound = Playsound1
    status_label.configure(text="Selected Sound: 1")

def play_sound2():
    global selected_sound
    selected_sound = playsound2
    status_label.configure(text="Selected Sound: 2")

# --- GUI Setup ---
import customtkinter as ctk

# Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk(fg_color="#12141A")
app.title("S.A.D.I.A.S.C.")
app.geometry("480x500")

# Style
button_color = "#15161D"
button_hover = "#1E1E1E"
active_border_color = "#454545"

# Title
ctk.CTkLabel(app, text="S.A.D.I.A.S.C.", font=ctk.CTkFont(size=28, weight="bold"), text_color="#83FF9E").pack(pady=(20, 5))

# Subtitle
ctk.CTkLabel(
    app,
    text="Smart Anomaly Detection Intelligence and Surveillance Camera",
    font=ctk.CTkFont(size=14),
    wraplength=400,
    justify="center",
    text_color="white"
).pack(pady=5)

# Camera Input
camera_entry = ctk.CTkEntry(app, placeholder_text="Enter Camera Index (e.g., 0)", fg_color=button_color, border_color=active_border_color)
camera_entry.pack(pady=15)

# Start Button
ctk.CTkButton(
    app,
    text="Start Detection",
    command=start_detection,
    fg_color=button_color,
    hover_color=button_hover,
    border_color=active_border_color,
    border_width=2
).pack(pady=10)

# Buttons Container
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=10)

# Row 0 - Sound buttons
ctk.CTkButton(button_frame, text="Sound 1", width=100, command=play_sound1, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=0, column=0, padx=10)
ctk.CTkButton(button_frame, text="Sound 2", width=100, command=play_sound2, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=0, column=1, padx=10)
ctk.CTkButton(button_frame, text="Sound 3", width=100, command=play_sound2, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=0, column=2, padx=10)

# Row 1 - Config buttons
ctk.CTkButton(button_frame, text="Configure Number", width=100, command=text_config, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=3, column=0, pady=10)
ctk.CTkButton(button_frame, text="Register Admin", width=100, command=admin_config, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=3, column=1, pady=10)

# Row 2 - Logs buttons
ctk.CTkButton(button_frame, text="Open Logs", width=100, command=logfun, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=2, column=0, pady=10)
ctk.CTkButton(button_frame, text="Open Numbers", width=100, command=textfun, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=2, column=1, pady=10)
ctk.CTkButton(button_frame, text="Open Admin Logs", width=100, command=seeadmin, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=2, column=2, pady=10)

# Sound Status
status_label = ctk.CTkLabel(app, text="Selected Sound: None", font=ctk.CTkFont(size=12), text_color="white")
status_label.pack(pady=(10, 0))

# Run
app.mainloop()

