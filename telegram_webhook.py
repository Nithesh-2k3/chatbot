import sqlite3
from flask import Flask, request
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
DATABASE = "cs_department.db"

# Fetch all intents and responses from DB once
def fetch_all_responses():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT intent, response FROM responses")
    data = cursor.fetchall()
    conn.close()
    return data

all_data = fetch_all_responses()
intents = [item[0] for item in all_data]
responses = {item[0]: item[1] for item in all_data}

# Use TF-IDF vectorizer
vectorizer = TfidfVectorizer().fit(intents)
intent_vectors = vectorizer.transform(intents)

def find_best_match(user_message):
    user_vec = vectorizer.transform([user_message])
    similarities = cosine_similarity(user_vec, intent_vectors)
    best_match_index = similarities.argmax()
    if similarities[0][best_match_index] > 0.3:
        return responses[intents[best_match_index]]
    return "Sorry, I don't understand that yet."

@app.route("/", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        response = find_best_match(user_message)
        send_message(chat_id, response)

    return "ok", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
