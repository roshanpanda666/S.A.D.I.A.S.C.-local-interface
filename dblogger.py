import os
import time
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load MongoDB credentials from .env
load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

# MongoDB connection string
client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.09x2u1i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Select DB and collection
db = client["sadiasc_logs"]
collection = db["detection_events"]

def push_latest_log():
    """
    Reads the last JSON line from log.txt and pushes it as structured data to MongoDB.
    """
    try:
        time.sleep(1)  # Optional delay

        with open("log.txt", "r") as file:
            # Remove empty lines and strip whitespace
            lines = [line.strip() for line in file.readlines() if line.strip()]
            
            if not lines:
                print("[DB Logger] No valid log lines found.")
                return

            last_line = lines[-1]

            try:
                log_data = json.loads(last_line)  # Convert JSON string to dict
            except json.JSONDecodeError:
                print("[DB Logger] Last line is not valid JSON.")
                return

            # Add current timestamp
            document = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "log": log_data
            }

            collection.insert_one(document)
            print("[DB Logger] Pushed log to MongoDB:\n", document)

    except Exception as e:
        print(f"[DB Logger Error] {e}")

# Optional for testing
if __name__ == "__main__":
    push_latest_log()
