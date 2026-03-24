import os
import requests
from flask import Flask, request, abort

TOKEN = os.environ["BOT_TOKEN"]
SECRET = os.environ["SECRET_TOKEN"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

WELCOME_MESSAGE = "Ciao 👋"

def tg(method, data):
    r = requests.post(f"{BASE_URL}/{method}", json=data, timeout=20)
    print("METHOD:", method)
    print("DATA:", data)
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)
    r.raise_for_status()
    return r.json()

@app.route("/", methods=["GET"])
def home():
    return "ok", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret != SECRET:
        abort(403)

    update = request.get_json(silent=True) or {}
    print("UPDATE:", update)

    join_request = update.get("chat_join_request")

    if join_request:
        chat_id = join_request["chat"]["id"]
        user_id = join_request["from"]["id"]
        user_chat_id = join_request["user_chat_id"]

        try:
            tg("sendMessage", {
                "chat_id": user_chat_id,
                "text": WELCOME_MESSAGE
            })
        except Exception as e:
            print("Errore invio messaggio:", e)

        try:
            tg("approveChatJoinRequest", {
                "chat_id": chat_id,
                "user_id": user_id
            })
        except Exception as e:
            print("Errore approvazione:", e)

    return "ok", 200
