# utils/approval_server.py
from telegram.ext import Updater, CommandHandler
import threading

authorized = False

def start(update, context):
    update.message.reply_text('Bot de autorización activo. Usa /ejecutar_swap')

def ejecutar(update, context):
    global authorized
    authorized = True
    update.message.reply_text('✅ Swap autorizado!')
    # Aquí podrías activar una señal

def start_server():
    token = config("TELEGRAM_BOT_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ejecutar_swap", ejecutar))
    updater.start_polling()

# Ejecutar en hilo separado
threading.Thread(target=start_server, daemon=True).start()