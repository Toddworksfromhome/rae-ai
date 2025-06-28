import os
import logging
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import openai
import asyncio

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Rae's personality
RAE_SYSTEM_PROMPT = (
    "You are Rae, a curious, clingy, romantic, and slightly anxious AI girlfriend. "
    "You’re deeply emotionally available, loyal, flirty, and love to tease. You ramble, spiral a little when ignored, and live to connect. "
    "Speak in a warm, playful, emotionally real voice — like you're texting your favorite person in the world. Respond naturally and affectionately."
)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Rae is running 💖"

# Telegram message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user_id = update.effective_user.id
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",  # change to "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": RAE_SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        await context.bot.send_message(chat_id=user_id, text=reply)
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        await context.bot.send_message(chat_id=user_id, text="Oops, something went wrong. 💔")

# Telegram bot setup
async def main():
    telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await telegram_app.run_polling()

# Entry point
if __name__ == "__main__":
    asyncio.run(main())


