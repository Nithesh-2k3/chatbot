import sqlite3
from flask import Flask, request
import requests
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7629694750:AAG6vET2cga29hi14V-9lh13ZJEPWSAkjDs"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Connect to database
conn = sqlite3.connect('cs_department.db', check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__)

# Function to get best-matching response using NLP
def get_best_response(user_input):
    user_doc = nlp(user_input)

    cursor.execute("SELECT intent, response FROM responses")
    all_data = cursor.fetchall()

    best_match = None
    highest_similarity = 0.0

    for intent, response in all_data:
        intent_doc = nlp(intent)
        similarity = user_doc.similarity(intent_doc)

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = response

    if highest_similarity > 0.75:
        return best_match
    else:
        return "Sorry, I don't understand that yet."

# Route to handle Telegram webhook
@app.route('/', methods=['POST'])
def telegram_webhook():
    data = request.json

    if 'message' in data and 'text' in data['message']:
        chat_id = data['message']['chat']['id']
        user_message = data['message']['text']

        bot_response = get_best_response(user_message)

        requests.post(TELEGRAM_API_URL, json={
            'chat_id': chat_id,
            'text': bot_response
        })

    return 'OK', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
