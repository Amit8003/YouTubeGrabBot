import os
import base64
import json
import logging
import firebase_admin
import requests
from firebase_admin import credentials, db
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔥 Firebase Setup (GitHub Secrets se Credentials Load karna)
firebase_base64 = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_base64:
    raise ValueError("❌ Error: FIREBASE_CREDENTIALS secret not found!")

firebase_json = base64.b64decode(firebase_base64).decode("utf-8")
cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {"databaseURL": "https://your-database-url.firebaseio.com/"})

# 🤖 Telegram Bot Token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Error: TELEGRAM_BOT_TOKEN secret not found!")

# 🔗 Rebrandly API Key
REBRANDLY_API_KEY = os.getenv("REBRANDLY_API_KEY")

# 🎵 YouTube Video Download Function
def get_youtube_download_link(video_url):
    try:
        api_url = f"https://your-api.com/download?url={video_url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get("download_link")
        else:
            return None
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return None

# 🔗 Shorten Link using Rebrandly
def shorten_link(long_url):
    if not REBRANDLY_API_KEY:
        return long_url  # Agar Rebrandly key nahi hai to original link return karo
    headers = {"Content-Type": "application/json", "apikey": REBRANDLY_API_KEY}
    data = json.dumps({"destination": long_url})
    response = requests.post("https://api.rebrandly.com/v1/links", headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("shortUrl", long_url)
    return long_url

# 🚀 Start Command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("👋 Welcome! Send me a YouTube link to download.")

# 🎬 YouTube Link Handler
async def youtube_handler(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    if "youtube.com" in message_text or "youtu.be" in message_text:
        await update.message.reply_text("🔄 Processing your request...")
        download_link = get_youtube_download_link(message_text)
        if download_link:
            short_link = shorten_link(download_link)
            keyboard = [[InlineKeyboardButton("⬇ Download Now", url=short_link)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("✅ Your download link is ready!", reply_markup=reply_markup)
        else:
            await update.message.reply_text("❌ Error: Could not fetch the download link.")
    else:
        await update.message.reply_text("❌ Please send a valid YouTube link.")

# 🚀 Telegram Bot Initialization
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("youtube", youtube_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
