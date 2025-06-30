import json
from datetime import datetime
import matplotlib.pyplot as plt

# Load log data
data = []
with open("log.txt", "r") as f:
    for line in f:
        try:
            entry = json.loads(line)
            data.append(entry)
        except:
            continue

# Filter only valid intruder detections with face detection
filtered = []
for entry in data:
    if (entry.get("face_detection") is True and 
        entry.get("detection") == "intruder" and 
        entry.get("time") and entry.get("camera") and entry.get("alarm")):
        try:
            time_obj = datetime.strptime(entry["time"], "%H:%M:%S")
            filtered.append({
                "time": time_obj,
                "camera": entry["camera"],
                "alarm": entry["alarm"]
            })
        except:
            continue

# Plot setup
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 6))

# Scatter points by alarm type
for alarm_type, color, marker in [
    ("playsound1", "cyan", "o"),
    ("playsound2", "orange", "x")
]:
    x = [entry["time"] for entry in filtered if entry["alarm"].lower() == alarm_type]
    y = [entry["camera"] for entry in filtered if entry["alarm"].lower() == alarm_type]
    if x:
        ax.scatter(x, y, label=f"{alarm_type}", color=color, marker=marker, s=80)

# Customize plot
ax.set_title("Intruder Detections by Camera and Alarm", fontsize=14)
ax.set_xlabel("Time", fontsize=12)
ax.set_ylabel("Camera ID", fontsize=12)
plt.xticks(rotation=45)
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()
