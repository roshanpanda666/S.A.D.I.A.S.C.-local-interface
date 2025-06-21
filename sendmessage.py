from twilio.rest import Client
from dotenv import load_dotenv
import os

# --- Load credentials from .env once ---
load_dotenv()
twilio_sid = os.getenv("TWILIO_SID")
twilio_token = os.getenv("TWILIO_TOKEN")
twilio_number = "+15076280790"

def send_intruder_alert():
    """
    Sends 'Intruder Detected' message to the number in numbers.txt using Twilio.
    """
    try:
        # Read recipient number from file
        with open("numbers.txt", "r") as file:
            recipient_number = file.readline().strip()
            if not recipient_number:
                raise ValueError("Phone number is empty in numbers.txt")
    except Exception as e:
        print(f"[S.A.D.I.A.S.C. ALERT ERROR] Failed to read number: {e}")
        return

    try:
        client = Client(twilio_sid, twilio_token)
        message = client.messages.create(
            body="⚠️ Intruder Detected by S.A.D.I.A.S.C.",
            from_=twilio_number,
            to=recipient_number
        )
        print(f"[S.A.D.I.A.S.C.] Alert sent to {recipient_number} ✅")
    except Exception as e:
        print(f"[S.A.D.I.A.S.C. ALERT ERROR] Failed to send message: {e}")
