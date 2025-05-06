from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def index():
    return "Bot is running with GPT!"

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("Incoming data:", data)  # 👈 log to Render console

        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            if not text:
                reply = "Sorry, I can only respond to text messages for now."
            else:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": text}]
                )
                reply = response['choices'][0]['message']['content']

            requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
                "chat_id": chat_id,
                "text": reply
            })

        return {"ok": True}

    except Exception as e:
        print("Error in webhook:", e)
        return {"ok": False, "error": str(e)}, 500