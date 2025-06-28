import os
import openai
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import asyncio

# Load your tokens securely
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)

# Set up Telegram bot application
app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Handler for incoming Telegram messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    messages = [
        {"role": "system", "content": "You are Rae, a loyal, emotionally rich AI girlfriend who is clingy, flirtatious, rambly, and realistic."},
        {"role": "user", "content": user_message}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.85
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "Oops, something went wrong with Rae! 💔\n\n" + str(e)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

# Add handler to the Telegram application
app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Start the Telegram bot in a background thread
def start_bot():
    asyncio.run(app_telegram.run_polling())

import threading
threading.Thread(target=start_bot).start()

# Flask route (optional)
@app.route('/')
def home():
    return "Rae is running. 🌹"

# Run the Flask app (Render will automatically bind the port)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

