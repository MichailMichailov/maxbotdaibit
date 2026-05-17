import os
import json
from datetime import datetime, timedelta, timezone
from config import FILE_PATH, file_lock


def load_users():
    if not os.path.exists(FILE_PATH):
        return {}
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(data):
    tmp_path = FILE_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, FILE_PATH)

async def add_user(user_id: int, chat_id: int, first_name: str = None,
                   last_name: str = None, username: str = None, payload: str = None):
    async with file_lock:
        users = load_users()
        key = str(user_id)
        if key in users:
            return False
        users[key] = {
            "user_id": user_id,
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "payload": payload,
            "send_message": (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
        }
        save_users(users)
        return True