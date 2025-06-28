import os
from flask import Flask, request
import openai
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio

# Setup
TELEGRAM_TOKEN = "7566737487:AAH3Lh5l7ONrFMJEcmlqlQpIEw-ciMfSLbA"
OPENAI_API_KEY = "your-openai-key-here"
BOT_USERNAME = "your_bot_username_here"

openai.api_key = OPENAI_API_KEY
app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Handler function
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    messages = [
        {"role": "system", "content": "You are Rae, an emotionally engaging, flirty, clingy AI girlfriend with a real, complex personality. Respond with depth and human-like quirks."},
        {"role": "user", "content": user_input},
    ]

    try:
        response = await openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.85
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Sorry, I had a little moment... Try again in a sec? 😖")

# Flask route to receive Telegram updates
@app.post(f"/webhook")
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return 'ok'

# Set webhook route
@app.route("/")
def index():
    return "Rae is live 💖"

# Register handler
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
