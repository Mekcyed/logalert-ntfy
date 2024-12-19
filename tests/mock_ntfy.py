from fastapi import FastAPI, Request
from typing import Dict

app = FastAPI()
notifications: Dict[str, list] = {}

@app.post("/{topic}")
async def receive_notification(topic: str, request: Request):
    body = await request.body()
    if topic not in notifications:
        notifications[topic] = []
    notifications[topic].append({
        "message": body.decode('utf-8'),
        "headers": dict(request.headers)
    })
    return {"message": "Notification received"}

@app.get("/{topic}/notifications")
def get_notifications(topic: str):
    return notifications.get(topic, [])
