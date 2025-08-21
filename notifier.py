# notifier.py
from decouple import config
import requests

def send_telegram(text):
    token = config("TELEGRAM_BOT_TOKEN")
    chat_id = config("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

def alert(message):
    send_telegram(message)