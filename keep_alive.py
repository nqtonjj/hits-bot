from flask import Flask, request
from threading import Thread
import json
import os
import requests
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = ["1924694116"]  # có thể thay bằng list từ file nếu cần
SENT_TASKS_FILE = "sent_tasks.json"

# Load task đã gửi
try:
    with open(SENT_TASKS_FILE, "r") as f:
        sent_tasks = json.load(f)
except:
    sent_tasks = []

KEYWORDS = ["VN", "EN-US", "Ads"]

@app.route("/")
def home():
    return "Bot HITs Telegram đang hoạt động!"

@app.route("/v1/notifications", methods=["POST"])
def receive_notification():
    data = request.get_json()
    hits = data.get("hits", [])

    new = False
    for hit in hits:
        task_id = str(hit.get("Id"))
        title = hit.get("FriendlyName", "")

        if task_id in sent_tasks:
            continue
        if not any(k.lower() in title.lower() for k in KEYWORDS):
            continue

        now = datetime.now().strftime("%H:%M")
        message = (
            f"🔔 New HIT Alert!\n"
            f"🆔 Task ID: {task_id}\n"
            f"📌 Title: {title}\n"
            f"🕓 Time: {now}\n"
            f"-- H.A Lite 🍀"
        )

        for chat_id in CHAT_IDS:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, data={'chat_id': chat_id, 'text': message})

        sent_tasks.append(task_id)
        new = True

    if new:
        with open(SENT_TASKS_FILE, "w") as f:
            json.dump(sent_tasks, f)

    return {"status": "ok"}, 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
