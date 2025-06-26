import customtkinter as ctk
import os

# --- Save email and password ---
def save_admin_details():
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if email and password:
        with open("admin-details.txt", "w") as f:
            f.write(f"{email}\n{password}\n")
        status_label.configure(text=f"Saved Email: {email}")
        email_entry.delete(0, ctk.END)
        password_entry.delete(0, ctk.END)
    else:
        status_label.configure(text="Both fields are required!")

# --- Style Variables ---
bg_color = "#12141A"
btn_color = "#15161D"
hover_color = "#83FF9E"
border_color = "#83FF9E"

# --- GUI Setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk(fg_color=bg_color)
app.title("S.A.D.I.A.S.C. Admin Saver")
app.geometry("400x350")

# Title
title_label = ctk.CTkLabel(app, text="S.A.D.I.A.S.C. Admin Saver",
                           font=ctk.CTkFont(size=22, weight="bold"), text_color="gray")
title_label.pack(pady=(20, 10))

# Subtitle
subtitle_label = ctk.CTkLabel(app, text="Enter email and password to register the admin", text_color="white")
subtitle_label.pack(pady=5)

# Email Entry Field
email_entry = ctk.CTkEntry(app,
                            placeholder_text="Enter E-mail (e.g., someone@gmail.com)",
                            width=300,
                            fg_color=btn_color,
                            border_color=border_color)
email_entry.pack(pady=10)

# Password Entry Field
password_entry = ctk.CTkEntry(app,
                               placeholder_text="Enter Password",
                               width=300,
                               show="*",
                               fg_color=btn_color,
                               border_color=border_color)
password_entry.pack(pady=10)

# Save Button
save_button = ctk.CTkButton(app,
                            text="Save Admin Details",
                            command=save_admin_details,
                            fg_color=btn_color,
                            hover_color=hover_color,
                            border_color=border_color,
                            border_width=2)
save_button.pack(pady=15)

# Status Label
status_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=12), text_color="white")
status_label.pack(pady=10)

app.mainloop()
