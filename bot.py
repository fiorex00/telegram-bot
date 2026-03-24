import os
import requests
from flask import Flask, request, abort

TOKEN = os.environ["BOT_TOKEN"]
SECRET = os.environ["SECRET_TOKEN"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

WELCOME_MESSAGE = "Ciao 👋"

def log(*args):
    print(*args, flush=True)

def tg(method, data):
    r = requests.post(f"{BASE_URL}/{method}", json=data, timeout=20)
    log("METHOD:", method)
    log("DATA:", data)
    log("STATUS:", r.status_code)
    log("RESPONSE:", r.text)
    r.raise_for_status()
    return r.json()

@app.route("/", methods=["GET"])
def home():
    log("HOME OK")
    return "ok", 200

@app.route("/test", methods=["GET"])
def test():
    log("TEST OK")
    return "test ok", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    log("WEBHOOK HIT")

    header_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    log("HEADER SECRET:", header_secret)

    if header_secret != SECRET:
        log("SECRET NON VALIDO")
        abort(403)

    update = request.get_json(silent=True) or {}
    log("UPDATE:", update)

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
            log("ERRORE INVIO MESSAGGIO:", e)

        try:
            tg("approveChatJoinRequest", {
                "chat_id": chat_id,
                "user_id": user_id
            })
        except Exception as e:
            log("ERRORE APPROVAZIONE:", e)

    return "ok", 200
