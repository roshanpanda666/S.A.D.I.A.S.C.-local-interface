import cv2
import threading
import customtkinter as ctk
from sound import Playsound1, playsound2  # Defined in sound.py
from datetime import datetime

def log_detection_data(sound_name, cam_index):
    now = datetime.now().strftime("%H:%M:%S")
    with open("log.txt", "a") as file:
        file.write(f"alarm: {sound_name}\n")
        file.write("face detection: true\n")
        file.write(f"time: {now}\n")
        file.write(f"camera: {cam_index}\n")
        file.write("____________________________\n")

        
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

            #after face got detected
            
            if len(faces) > 0 and not sound_played:
                sound_played = True
                if selected_sound is not None:
                    threading.Thread(target=selected_sound, daemon=True).start()
                    log_detection_data(
                    sound_name=selected_sound.__name__,
                    cam_index=cam_index
                    )
            elif len(faces) == 0:
                sound_played = False

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)

            cv2.putText(frame, "Press Q to exit", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.imshow("Face Detection with Sound", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=detection, daemon=True).start()

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
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("S.A.D.I.A.S.C.")
app.geometry("480x420")

# Title
title_label = ctk.CTkLabel(app, text="S.A.D.I.A.S.C.", font=ctk.CTkFont(size=28, weight="bold"))
title_label.pack(pady=(20, 5))

# Subtitle
subtitle_label = ctk.CTkLabel(app, text="Smart Anomaly Detection Intelligence and Surveillance Camera",
                              font=ctk.CTkFont(size=14), wraplength=400, justify="center")
subtitle_label.pack(pady=5)

# Camera Entry
camera_entry = ctk.CTkEntry(app, placeholder_text="Enter Camera Index (e.g., 0)")
camera_entry.pack(pady=15)

# Start Detection Button
start_button = ctk.CTkButton(app, text="Start Detection", command=start_detection)
start_button.pack(pady=10)

# Sound Buttons
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=10)

sound1_button = ctk.CTkButton(button_frame, text="Sound 1", width=100, command=play_sound1)
sound1_button.grid(row=0, column=0, padx=10)

sound2_button = ctk.CTkButton(button_frame, text="Sound 2", width=100, command=play_sound2)
sound2_button.grid(row=0, column=1, padx=10)

# Sound Status Label
status_label = ctk.CTkLabel(app, text="Selected Sound: None", font=ctk.CTkFont(size=12))
status_label.pack(pady=(10, 0))

# Run the app
app.mainloop()
