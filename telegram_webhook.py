import sqlite3
import requests
from flask import Flask, request

app = Flask(__name__)

# Your Telegram Bot Token
BOT_TOKEN = "7629694750:AAG6vET2cga29hi14V-9lh13ZJEPWSAkjDs"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Get answer from the SQLite DB based on user message
def get_response_from_db(user_message):
    conn = sqlite3.connect('cs_department.db')
    cursor = conn.cursor()

    cursor.execute("SELECT response FROM responses WHERE LOWER(intent) LIKE ?", ('%' + user_message.lower() + '%',))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return "Sorry, I don't understand that yet."

# Handle POST request from Telegram
@app.route('/', methods=['POST'])
def telegram_webhook():
    data = request.get_json()

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        user_message = data['message'].get('text', '')

        # Get bot response
        bot_response = get_response_from_db(user_message)

        # Send message back to Telegram
        requests.post(TELEGRAM_API_URL, json={
            'chat_id': chat_id,
            'text': bot_response
        })

    return "OK", 200

# Start Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
