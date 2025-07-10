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
import time
from pushsettingdata import push_last_setting_to_mongo
# --- Logging Setting Change ---
def log_setting_change(action_type, value=None):
    log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action_type,
        "value": value
    }

    with open("settings-data.txt", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print("[Settings Logger] Entry:", log_entry)

    time.sleep(1)

    push_last_setting_to_mongo()

# --- Log Detection Data ---
def log_detection_data(sound_name, cam_index):
    now = datetime.now().strftime("%H:%M:%S")

    try:
        with open("numbers.txt", "r") as number_file:
            phone_number = number_file.readline().strip()
    except FileNotFoundError:
        phone_number = "Not available"

    log_data = {
        "alarm": sound_name,
        "face_detection": True,
        "detection": "intruder",
        "camera": cam_index,
        "number": phone_number,
        "time": now
    }

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

    log_setting_change("detection_started", f"Camera {cam_index}")

    def detection():
        global sound_played

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

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

# --- Configuration Shortcuts ---
def text_config():
    log_setting_change("open_config", "textsetting.py")
    subprocess.Popen(["python", "textsetting.py"])

def admin_config():
    log_setting_change("open_config", "admin_pwdchange.py")
    subprocess.Popen(["python", "admin_pwdchange.py"])

def logfun():
    log_setting_change("open_file", "log.txt")
    subprocess.Popen(["notepad.exe", "log.txt"])

def seeadmin():
    log_setting_change("open_file", "admin-details.txt")
    subprocess.Popen(["notepad.exe", "admin-details.txt"])

def textfun():
    log_setting_change("open_file", "numbers.txt")
    subprocess.Popen(["notepad.exe", "numbers.txt"])

def seeplot():
    log_setting_change("run_script", "plot.py")
    subprocess.Popen(["python", "plot.py"])

def seecmd():
    log_setting_change("open_cmd", "cmd")
    subprocess.Popen("start cmd", shell=True)

# --- Sound Selection Buttons ---
def play_sound1():
    global selected_sound
    selected_sound = Playsound1
    status_label.configure(text="Selected Sound: 1")
    log_setting_change("sound_selected", "Playsound1")

def play_sound2():
    global selected_sound
    selected_sound = playsound2
    status_label.configure(text="Selected Sound: 2")
    log_setting_change("sound_selected", "playsound2")

# --- GUI Setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk(fg_color="#12141A")
app.title("S.A.D.I.A.S.C.")
app.geometry("480x500")

button_color = "#15161D"
button_hover = "#1E1E1E"
active_border_color = "#454545"

ctk.CTkLabel(app, text="S.A.D.I.A.S.C.", font=ctk.CTkFont(size=28, weight="bold"), text_color="#83FF9E").pack(pady=(20, 5))

ctk.CTkLabel(
    app,
    text="Smart Anomaly Detection Intelligence and Surveillance Camera",
    font=ctk.CTkFont(size=14),
    wraplength=400,
    justify="center",
    text_color="white"
).pack(pady=5)

camera_entry = ctk.CTkEntry(app, placeholder_text="Enter Camera Index (e.g., 0)", fg_color=button_color, border_color=active_border_color)
camera_entry.pack(pady=15)

ctk.CTkButton(
    app,
    text="Start Detection",
    command=start_detection,
    fg_color=button_color,
    hover_color=button_hover,
    border_color=active_border_color,
    border_width=2
).pack(pady=10)

button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text="Sound 1", width=100, command=play_sound1, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=0, column=0, padx=10)

ctk.CTkButton(button_frame, text="Sound 2", width=100, command=play_sound2, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=0, column=1, padx=10)

ctk.CTkButton(button_frame, text="Sound 3", width=100, command=play_sound2, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=0, column=2, padx=10)

ctk.CTkButton(button_frame, text="Configure Number", width=100, command=text_config, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=3, column=0, pady=10)

ctk.CTkButton(button_frame, text="Register Admin", width=100, command=admin_config, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=3, column=1, pady=10)

ctk.CTkButton(button_frame, text="Open Logs", width=100, command=logfun, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=2, column=0, pady=10)

ctk.CTkButton(button_frame, text="Open Numbers", width=100, command=textfun, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=2, column=1, pady=10)

ctk.CTkButton(button_frame, text="Open Admin Logs", width=100, command=seeadmin, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=2, column=2, pady=10)

ctk.CTkButton(button_frame, text="open detection plot", width=100, command=seeplot, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=3, column=2, pady=10)

ctk.CTkButton(button_frame, text="open shell </>", width=100, command=seecmd, fg_color=button_color,
              hover_color=button_hover, border_color=active_border_color, border_width=2).grid(row=4, column=0, pady=10)

status_label = ctk.CTkLabel(app, text="Selected Sound: None", font=ctk.CTkFont(size=12), text_color="white")
status_label.pack(pady=(10, 0))

app.mainloop()
