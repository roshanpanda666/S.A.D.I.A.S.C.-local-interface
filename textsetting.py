import customtkinter as ctk
from dotenv import load_dotenv
import os

# --- Load Twilio credentials from .env ---
load_dotenv()  # This loads environment variables from .env into the OS environment
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

# --- GUI Setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("S.A.D.I.A.S.C. Contact Saver")
app.geometry("400x300")

# Title
title_label = ctk.CTkLabel(app, text="S.A.D.I.A.S.C. Contact Saver", font=ctk.CTkFont(size=22, weight="bold"))
title_label.pack(pady=(20, 10))

# Subtitle
subtitle_label = ctk.CTkLabel(app, text="Enter a phone number to save to numbers.txt")
subtitle_label.pack(pady=5)

# Entry Field
number_entry = ctk.CTkEntry(app, placeholder_text="Enter phone number (e.g., +91XXXXXXXXXX)", width=300)
number_entry.pack(pady=15)

# Save Button
save_button = ctk.CTkButton(app, text="Save Number", command=save_number)
save_button.pack(pady=10)

# Status
status_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=12))
status_label.pack(pady=10)

# Twilio SID Info (optional)
sid_label = ctk.CTkLabel(app, text=f"SID Loaded: {twilio_sid[:8]}..." if twilio_sid else "No Twilio SID loaded",
                         font=ctk.CTkFont(size=10))
sid_label.pack(pady=5)

app.mainloop()
