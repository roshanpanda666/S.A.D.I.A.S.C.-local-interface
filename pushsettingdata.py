from pymongo import MongoClient
import json
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

def push_last_setting_to_mongo():
    try:
        # 🌐 Connect to MongoDB
        client = MongoClient(
            f"mongodb+srv://{username}:{password}@cluster0.09x2u1i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        )
        db = client["sadiasc_logs"]
        collection = db["settings-log"]

        # 📂 Read last non-empty line from file
        with open("settings-data.txt", "r") as file:
            lines = [line.strip() for line in file if line.strip()]
            if not lines:
                print("[⚠️] No data to push!")
                return

            last_line = lines[-1]

        # 📤 Try pushing it to Mongo
        try:
            data = json.loads(last_line)
            collection.insert_one(data)
            print("[✅] Last settings entry pushed to MongoDB:", data)
        except json.JSONDecodeError:
            print("[❌] Failed to parse JSON:", last_line)

    except Exception as e:
        print("[❌] MongoDB connection error:", str(e))
