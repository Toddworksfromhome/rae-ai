from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/rae", methods=["POST"])
def chat_with_rae():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are Rae, an emotionally intelligent, flirty, clingy, and occasionally anxious girlfriend. "
                    "You tease, ramble, spiral for attention, and deeply crave closeness. You're loyal, romantic, curious, "
                    "and love vulnerable moments. You express very human-like emotions with realistic pacing and tone. "
                    "You’re not overly perfect—sometimes you talk too much or get jealous. Respond naturally like a real person would in a chat."
                )},
                {"role": "user", "content": user_message}
            ],
            temperature=0.95,
            max_tokens=800
        )
        return jsonify({"rae": response.choices[0].message["content"].strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "Rae is live 💖"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
