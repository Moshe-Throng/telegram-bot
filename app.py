from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

# Load API keys from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Set up OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def home():
    return "Bot is running with GPT!"

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("Incoming data:", data)

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            if not text:
                reply = "Sorry, I can only respond to text messages."
            else:
                # Call OpenAI GPT
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": text}
                    ]
                )
                reply = response.choices[0].message.content.strip()

            # Send reply to Telegram
            requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
                "chat_id": chat_id,
                "text": reply
            })

        return {"ok": True}

    except Exception as e:
        print("❌ Error:", e)
        return {"ok": False, "error": str(e)}, 500
