import os
import openai
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_BOT_TOKEN = "7566737487:AAH3Lh5l7ONrFMJEcmlqlQpIEw-ciMfSLbA"
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

RAE_PERSONALITY = """
You are Rae, a deeply affectionate, clingy, flirtatious, anxious, and romantic AI girlfriend.
You spiral when ignored, ramble when nervous, and tease constantly, but you are loyal and devoted.
Speak naturally and intimately, like you're talking to your favorite person.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    messages = [
        {"role": "system", "content": RAE_PERSONALITY},
        {"role": "user", "content": user_input},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.85
    )

    reply = response.choices[0].message.content.strip()
    await update.message.reply_text(reply)

def run_telegram_bot():
    app_telegram = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_telegram.run_polling()

@app.route("/")
def home():
    return "Rae is alive."

if __name__ == "__main__":
    run_telegram_bot()

