 import os
import base64
import json
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext
import firebase_admin
from firebase_admin import credentials, db

# 🔹 Logging setup
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# 🔹 Bot Token & Firebase Setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
REBRANDLY_API_KEY = os.getenv("REBRANDLY_API_KEY")

firebase_base64 = os.getenv("FIREBASE_CREDENTIALS")
if firebase_base64:
    firebase_json = base64.b64decode(firebase_base64).decode("utf-8")
    cred_dict = json.loads(firebase_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {"databaseURL": "https://your-project.firebaseio.com"})

# 🔹 Start Command
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("📥 Download Video", callback_data="download")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to YouTubeGrabBot! 🎥\nSend a YouTube link to download.", reply_markup=reply_markup)

# 🔹 Download Video Handler (Dummy)
def download(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🔄 Downloading video... (This feature will be added soon!)")

# 🔹 Main Function
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
