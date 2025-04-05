from flask import Flask, request
import sqlite3
import requests
import spacy

app = Flask(__name__)
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace with your bot token
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Load the medium spaCy model
nlp = spacy.load("en_core_web_md")

def get_response_from_db(user_message):
    conn = sqlite3.connect("cs_department.db")
    cursor = conn.cursor()

    cursor.execute("SELECT intent, response FROM responses")
    data = cursor.fetchall()
    conn.close()

    best_intent = None
    best_score = 0.7  # similarity threshold

    user_doc = nlp(user_message)

    for intent, response in data:
        intent_doc = nlp(intent)
        score = user_doc.similarity(intent_doc)
        if score > best_score:
            best_score = score
            best_intent = response

    if best_intent:
        return best_intent
    else:
        return "Sorry, I don't understand that yet."

@app.route("/", methods=["POST"])
def telegram_webhook():
    data = request.json
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        bot_response = get_response_from_db(user_message)

        requests.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": bot_response
        })

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
