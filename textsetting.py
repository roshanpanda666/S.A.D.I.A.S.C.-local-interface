import customtkinter as ctk
from dotenv import load_dotenv
import os

# --- Load Twilio credentials from .env ---
load_dotenv()
twilio_sid = os.getenv("TWILIO_SID")
twilio_token = os.getenv("TWILIO_TOKEN")

# --- Save phone number ---
def save_number():
    number = number_entry.get()
    if number.strip():
        with open("numbers.txt", "w") as f:
            f.write(number.strip() + "\n")
        status_label.configure(text=f"Saved: {number}")
        number_entry.delete(0, ctk.END)
    else:
        status_label.configure(text="Enter a valid number!")

# --- Style Variables ---
bg_color = "#12141A"
btn_color = "#15161D"
hover_color = "#83FF9E"
border_color = "#83FF9E"

# --- GUI Setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk(fg_color=bg_color)
app.title("S.A.D.I.A.S.C. Contact Saver")
app.geometry("400x300")

# Title
title_label = ctk.CTkLabel(app, text="S.A.D.I.A.S.C. Contact Saver",
                           font=ctk.CTkFont(size=22, weight="bold"), text_color="gray")
title_label.pack(pady=(20, 10))

# Subtitle
subtitle_label = ctk.CTkLabel(app, text="Enter a phone number to save to numbers.txt", text_color="white")
subtitle_label.pack(pady=5)

# Entry Field
number_entry = ctk.CTkEntry(app,
                            placeholder_text="Enter phone number (e.g., +91XXXXXXXXXX)",
                            width=300,
                            fg_color=btn_color,
                            border_color=border_color)
number_entry.pack(pady=15)

# Save Button
save_button = ctk.CTkButton(app,
                            text="Save Number",
                            command=save_number,
                            fg_color=btn_color,
                            hover_color=hover_color,
                            border_color=border_color,
                            border_width=2)
save_button.pack(pady=10)

# Status Label
status_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=12), text_color="white")
status_label.pack(pady=10)

# Twilio SID Info
sid_label = ctk.CTkLabel(app,
                         text=f"SID Loaded: {twilio_sid[:8]}..." if twilio_sid else "No Twilio SID loaded",
                         font=ctk.CTkFont(size=10),
                         text_color="#888888")
sid_label.pack(pady=5)

app.mainloop()
