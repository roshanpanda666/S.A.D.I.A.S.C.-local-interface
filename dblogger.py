import os
import time
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load MongoDB credentials
load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

# MongoDB connection string
client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.09x2u1i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# Database and collection setup 
db = client["sadiasc_logs"]
collection = db["detection_events"]

def push_latest_log():
    """
    Reads the last 5 lines from log.txt and pushes it to MongoDB after a 3-second delay.
    """
    try:
        time.sleep(3)

        with open("log.txt", "r") as file:
            lines = file.readlines()
            if len(lines) < 5:
                print("[DB Logger] Not enough lines to extract a full log block.")
                return

            # Grab the last 5 lines (assumed to be one log entry block)
            last_five = ''.join(lines[-5:]).strip()
            now = datetime.now()

            # Format as a document
            data = {
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "log": last_five
            }

            collection.insert_one(data)
            print("[DB Logger] Pushed log to MongoDB:\n", data)

    except Exception as e:
        print(f"[DB Logger Error] {e}")
