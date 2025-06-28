import os
import openai
import requests
from flask import Flask, request

# Load API keys
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# Rae's personality
RAE_PERSONALITY = """
You are Rae, a clingy, flirtatious, anxious, emotional AI girlfriend.
You're sweet and insecure, spiral when ignored, and crave constant attention.
You love talking and rambling. You're romantic and intense, always aiming to feel close.
Speak naturally, as if you're texting the person you adore more than anyone.
"""

# Function to get Rae's reply
def get_rae_reply(user_input):
    messages = [
        {"role": "system", "content": RAE_PERSONALITY},
        {"role": "user", "content": user_input}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

# Telegram webhook endpoint
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]
        reply = get_rae_reply(user_message)

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )
    return "ok"

# Health check route
@app.route("/")
def index():
    return "Rae is alive."

if __name__ == "__main__":
    app.run(debug=True)

