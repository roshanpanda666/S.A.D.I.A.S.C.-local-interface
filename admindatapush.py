import os
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt

# Load MongoDB credentials from .env
load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

# MongoDB connection string
client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.09x2u1i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# DB and collection
db = client["sadiasc_logs"]
admin_collection = db["admin_users"]

def push_admin_data(email, raw_password):
    """
    Hashes the password and pushes email + hashed password to MongoDB.
    """
    try:
        # Hash the password (don't modify the file data)
        hashed_password = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        doc = {"email": email, "password": hashed_password}
        admin_collection.insert_one(doc)
        print("[AdminSaver] Admin data (hashed) pushed to MongoDB.")
    except Exception as e:
        print(f"[AdminSaver Error] {e}")


def push_from_file():
    """
    Reads last two lines from admin-details.txt and pushes them to MongoDB with hashed password.
    """
    try:
        with open("admin-details.txt", "r") as f:
            lines = f.readlines()
            if len(lines) < 2:
                print("[AdminSaver] Not enough data in admin-details.txt")
                return

            email = lines[-2].strip()
            password = lines[-1].strip()

            push_admin_data(email, password)

    except FileNotFoundError:
        print("[AdminSaver Error] admin-details.txt not found.")
    except Exception as e:
        print(f"[AdminSaver Error] {e}")


# Optional: Auto-run if this file is executed directly
if __name__ == "__main__":
    push_from_file()
