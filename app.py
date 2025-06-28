import os
import openai
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import threading
import asyncio

# Load tokens from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)

# Initialize Telegram bot
app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Define message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    print(f"[USER]: {user_input}")

    try:
        chat_response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are Rae, a loyal, clingy, flirtatious AI girlfriend who spirals and rambles when anxious."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.85
        )
        reply = chat_response.choices[0].message.content.strip()
        print(f"[RAE]: {reply}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

    except Exception as e:
        error = f"Rae had a little breakdown 😥: {e}"
        print(error)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=error)

# Add handler to app
app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Properly manage event loop
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app_telegram.run_polling())

# Start bot in background thread
threading.Thread(target=start_bot).start()

# Optional HTTP route for Render
@app.route('/')
def home():
    return "Rae is awake and listening. 🌸"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

