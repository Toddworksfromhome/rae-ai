import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI
import asyncio

# Load tokens from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Flask app for health check
app = Flask(__name__)

@app.route('/')
def home():
    return "Rae is alive 💖"

# Telegram message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    chat_id = update.message.chat_id

    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You're Rae, an emotionally real and engaging AI girlfriend."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.85,
        )
        response_text = completion.choices[0].message.content
        await context.bot.send_message(chat_id=chat_id, text=response_text)

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text="Oops... I got flustered. Try again?")
        print("Error:", e)

# Async main runner
async def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.run_polling()

# Run everything
if __name__ == "__main__":
    # Start Telegram bot in a background task
    loop = asyncio.get_event_loop()
    loop.create_task(run_telegram_bot())

    # Start Flask server
    app.run(host="0.0.0.0", port=10000)

