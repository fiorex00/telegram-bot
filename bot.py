import os
import requests
from flask import Flask, request, abort

# prende i dati da Render
TOKEN = os.environ["BOT_TOKEN"]
SECRET = os.environ["SECRET_TOKEN"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

# immagine
IMAGE_URL = "https://i.postimg.cc/52QtwC6P/Picsart-26-01-29-14-48-17-486(1).jpg"

# link del bottone
BUTTON_URL = "https://onlyfans.com/lucreziaboratti/c15"

def tg(method, data):
    r = requests.post(f"{BASE_URL}/{method}", json=data, timeout=20)
    print("METHOD:", method, flush=True)
    print("DATA:", data, flush=True)
    print("STATUS:", r.status_code, flush=True)
    print("RESPONSE:", r.text, flush=True)
    r.raise_for_status()
    return r.json()

@app.route("/", methods=["GET"])
def home():
    return "ok", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    header_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if header_secret != SECRET:
        abort(403)

    update = request.get_json(silent=True) or {}
    print("UPDATE:", update, flush=True)

    join_request = update.get("chat_join_request")

    if join_request:
        chat_id = join_request["chat"]["id"]
        user_id = join_request["from"]["id"]
        user_chat_id = join_request["user_chat_id"]

        user_name = join_request["from"].get("first_name", "amore")

        welcome_message = (
            f"Ei {user_name} ho una voglia assurda di divertirmi con te 🔞❤️\n\n"
            "Non fare il timido e entra qui sotto se vuoi sborrare, mando una foto gratis ai primi 5 che mi scrivono 😉\n\n"
        )

        # invia immagine + testo sotto + bottone
        try:
            tg("sendPhoto", {
                "chat_id": user_chat_id,
                "photo": IMAGE_URL,
                "caption": welcome_message,
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {
                                "text": "👉 CLICCA QUI 👈",
                                "url": BUTTON_URL
                            }
                        ]
                    ]
                }
            })
        except Exception as e:
            print("Errore invio messaggio:", e, flush=True)

        # approva automaticamente la richiesta
        try:
            tg("approveChatJoinRequest", {
                "chat_id": chat_id,
                "user_id": user_id
            })
        except Exception as e:
            print("Errore approvazione:", e, flush=True)

    return "ok", 200
