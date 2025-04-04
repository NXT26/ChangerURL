import json
import os
import random
import string

DB_FILE =  "data.json"
url_db = {}

def generate_short_code(length: int = 6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def save_db():
    serializable_db = {
        code: {
            "url": str(entry["url"]),
            "clicks": entry["clicks"]
        }
        for code, entry in url_db.items()
    }

    with open(DB_FILE, "w") as f:
        json.dump(serializable_db, f)

def load_db():
    global url_db
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            url_db = json.load(f)