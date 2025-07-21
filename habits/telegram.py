import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


def send_telegram_message(chat_id, text):
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не задан в переменных окружения")
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(TELEGRAM_API_URL, data=data)
    response.raise_for_status()
