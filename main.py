from dotenv import load_dotenv
import os
import json
import time
import requests
from keep_alive import keep_alive
from datetime import datetime

load_dotenv()

# Telegram config (ẩn bằng biến môi trường)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# File log task đã gửi
SENT_TASKS_FILE = 'sent_tasks.json'

# Tạo file nếu chưa có
try:
    with open(SENT_TASKS_FILE, 'r') as f:
        sent_tasks = json.load(f)
except:
    sent_tasks = []
    with open(SENT_TASKS_FILE, 'w') as f:
        json.dump(sent_tasks, f)


def send_telegram(task_id, title):
    now = datetime.now().strftime("%H:%M")
    message = (f"🔔 New HIT Alert!\n"
               f"🆔 Task ID: {task_id}\n"
               f"📌 Title: {title}\n"
               f"🕓 Time: {now}\n"
               f"-- H.A Lite 🍀")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message})


def check_hit():
    fake_hits = [
        {"id": 1001, "title": "Search Engine Judging (EN-US)"},
        {"id": 1002, "title": "Web Page Quality (VN)"},
        {"id": 1003, "title": "Ad Relevance Judging"},
    ]
    new = []
    for hit in fake_hits:
        if hit["id"] not in sent_tasks:
            send_telegram(hit["id"], hit["title"])
            sent_tasks.append(hit["id"])
            new.append(hit["id"])
    if new:
        with open(SENT_TASKS_FILE, 'w') as f:
            json.dump(sent_tasks, f)


keep_alive()

while True:
    check_hit()
    print("✅ Đã kiểm tra HITs")
    time.sleep(60)
