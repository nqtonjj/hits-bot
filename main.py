from flask import request
import json
import os
import requests

# Đảm bảo bạn đã load sent_tasks từ file
SENT_TASKS_FILE = "sent_tasks.json"
try:
    with open(SENT_TASKS_FILE, "r") as f:
        sent_tasks = json.load(f)
except:
    sent_tasks = []

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = ["1924694116"]  # hoặc đọc từ file chat_ids.json nếu cần

KEYWORDS = ["VN", "EN-US", "Ads"]  # ngươi muốn lọc gì thì chỉnh ở đây

def send_telegram(task_id, title):
    from datetime import datetime
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
        requests.post(url, data={"chat_id": chat_id, "text": message})

@app.route('/v1/notifications', methods=['POST'])
def notify_hits():
    data = request.get_json()
    hits = data.get("hits", [])

    new_sent = False
    for hit in hits:
        task_id = str(hit.get("Id"))
        title = hit.get("FriendlyName", "")

        if task_id in sent_tasks:
            continue

        # Lọc từ khóa
        if not any(kw.lower() in title.lower() for kw in KEYWORDS):
            continue

        send_telegram(task_id, title)
        sent_tasks.append(task_id)
        new_sent = True

    # Ghi lại những task mới đã gửi
    if new_sent:
        with open(SENT_TASKS_FILE, "w") as f:
            json.dump(sent_tasks, f)

    return {"status": "ok"}, 200
