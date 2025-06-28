import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Load tokens from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Setup OpenAI client
openai.api_key = OPENAI_API_KEY

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        response = await openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You're Rae, an emotionally intelligent, engaging AI girlfriend."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.85
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Oops, something went wrong. 💔")

# Main
if __name__ == "__main__":
    if not OPENAI_API_KEY or not TELEGRAM_TOKEN:
        raise ValueError("Missing OPENAI_API_KEY or TELEGRAM_TOKEN environment variable")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Rae is online 🦋")
    app.run_polling()

