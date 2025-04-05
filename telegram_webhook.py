from flask import Flask, request
import sqlite3
import requests

app = Flask(__name__)

# 🔐 Your Telegram Bot Token
TOKEN = "7629694750:AAG6vET2cga29hi14V-9lh13ZJEPWSAkjDs"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# 📦 Get response from 'responses' table in SQLite
def get_response_from_db(user_message):
    conn = sqlite3.connect("cs_department.db")
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM responses WHERE intent LIKE ?", ('%' + user_message + '%',))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "❌ Sorry, I don't understand that yet."

# 📬 Telegram webhook route
@app.route("/", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"].get("text", "")

        # Get response and reply to user
        bot_reply = get_response_from_db(user_message)
        requests.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": bot_reply
        })

    return "OK", 200

# 🚀 For local testing (optional)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
