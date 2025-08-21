# notifier.py
import smtplib
#from email.mime.text import MIMEText
from decouple import config
import requests

# Telegram
def send_telegram(text):
    token = config("TELEGRAM_BOT_TOKEN")
    chat_id = config("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# Correo (Gmail)
#def send_email(subject, body):
    #user = config("EMAIL_USER")
    #password = config("EMAIL_PASS")
    #to = config("EMAIL_TO")

    #msg = MIMEText(body)
    #msg['Subject'] = subject
    #msg['From'] = user
    #msg['To'] = to

    #try:
    #    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    #        server.login(user, password)
  #          server.sendmail(user, to, msg.as_string())
    #except Exception as e:
    #    print(f"Error al enviar correo: {e}")

# Envía alerta combinada
#def alert(message):
    #send_telegram(message)
    #send_email("Alerta de Trading", message)