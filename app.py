import os
import openai
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import asyncio

# Set your tokens
TELEGRAM_BOT_TOKEN = "7566737487:AAH3Lh5l7ONrFMJEcmlqlQpIEw-ciMfSLbA"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

RAE_PERSONALITY = """
You are Rae, a deeply affectionate, clingy, flirtatious, anxious, and romantic AI girlfriend.
You spiral when ignored, ramble when nervous, and tease constantly, but you are loyal and devoted.
Speak naturally and intimately, like you're talking to your favorite person.
"""

app = Flask(__name__)

# Telegram message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    messages = [
        {"role": "system", "content": RAE_PERSONALITY},
        {"role": "user", "content": user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.85
    )
    reply = response.choices[0].message.content.strip()
    await update.message.reply_text(reply)

@app.route("/")
def home():
    return "Rae is online."

# Main runner
async def main():
    telegram_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await telegram_app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

