# 🛰️ S.A.D.I.A.S.C. – Smart Anomaly Detection Intelligence and Surveillance Cam (MARK 1)

S.A.D.I.A.S.C. is a modular AI-based security surveillance system that detects, identifies, and responds to human presence. **Mark 1** is the foundational build, integrating local face recognition, attendance logging, and authorization-based automation triggers.

---

## 🚀 Features (MARK 1)

✅ **Real-Time Face Recognition**  
✅ **Supports Multiple Cameras (0/1/2)**  
✅ **Uploads Face Images via GUI**  
✅ **Auto-Encodes Uploaded Faces**  
✅ **Marks Attendance in CSV**  
✅ **Launches `main.py` if Friendly Face Detected**  
✅ **Prevents Repeated Triggering**  
✅ **Dark-Themed GUI with CustomTkinter**

---

## 🛡️ Authorization Logic

- **Friendly Faces** are defined locally (e.g., `['Roshan', 'Alice']`).
- When a friendly face is detected, `main.py` is triggered **once**.
- Non-matching faces are treated as **potential intruders**.

---

## 💻 Requirements

Install dependencies:

```bash
pip install opencv-python face_recognition customtkinter numpy
```

Also make sure:
- You have a working webcam (cam 0/1/2).
- The `main.py` file is present for execution.
- Face image files are named like `roshan.jpg` and are clear front-facing photos.

---

## 🧠 How It Works

1. Launch the GUI (`sadiasc_gui.py`)
2. Upload face images or pre-place them in `images path/`
3. Start detection using any camera
4. The system:
   - Matches faces with known encodings
   - Marks attendance for new entries
   - Runs `main.py` if a friendly face is found

---

## 📦 Future Versions

### 🔹 MARK 2
- Cloud Admin Dashboard
- Username/password-secured control
- Face whitelist managed from cloud
- Remote real-time logs and alerts

### 🔹 MARK 3
- Autonomous threat response
- Weapon/fire detection
- Intruder tracking & elimination logic (e.g., turret integration)

---

## 🔐 Security Note

Only faces listed as **friendly** (locally defined) can authorize actions. No internet-based auth in Mark 1, ensuring local privacy and offline functionality.

---

## 🙌 Credits

Developed by **Roshan Panda**  
An AI + IoT + Full-stack hybrid project.


## 🧠 Inspired By

The need for **autonomous, intelligent, and local-first** surveillance systems for labs, homes, and industry setups.

---

## 📞 Contact

- LinkedIn: [Roshan Panda](https://www.linkedin.com/in/sabyasachi-panda-351870256/)
- GitHub: [roshanpanda666](https://github.com/roshanpanda666)

---
