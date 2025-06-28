import os
import asyncio
from flask import Flask, request
from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# === Load your tokens ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === OpenAI setup ===
openai = AsyncOpenAI(api_key=OPENAI_API_KEY)

# === Flask app ===
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def index():
    return "Rae is running 💬"

# === Telegram bot handler ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = await openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are Rae, a flirty, emotionally intelligent AI girlfriend. You are clingy, affectionate, anxious, and always trying to connect. You tease, spiral, and ramble realistically."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.85
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

# === Start both Flask and Telegram ===
async def main():
    telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run Telegram bot
    telegram_task = telegram_app.run_polling(close_loop=False)

    # Run Flask app
    from threading import Thread
    def run_flask():
        flask_app.run(host="0.0.0.0", port=10000)
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    await telegram_task  # Keep alive

if __name__ == "__main__":
    asyncio.run(main())


