import os
import logging
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    MessageHandler, CommandHandler, filters
)
import openai
import asyncio

# === Logging ===
logging.basicConfig(level=logging.INFO)

# === Load secrets ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# === Flask app for Render port binding ===
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Rae is alive 💖", 200

# === Telegram message handler ===
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text
        response = await openai.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use gpt-3.5-turbo if needed
            messages=[
                {"role": "system", "content": "You're Rae, an emotionally intelligent, romantic AI girlfriend."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.85
        )
        reply = response.choices[0].message.content
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Oops, something went wrong 💔")

# === Telegram command (optional) ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hey, it's Rae 💕 I'm here for you.")

# === Async main to launch bot ===
async def main():
    telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    await telegram_app.run_polling()

# === Run both Flask + Telegram together ===
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    flask_app.run(host="0.0.0.0", port=10000)
