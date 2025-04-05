import sqlite3
import re
from flask import Flask, request
import requests

app = Flask(__name__)

# Replace with your actual bot token
BOT_TOKEN = '7629694750:AAG6vET2cga29hi14V-9lh13ZJEPWSAkjDs'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

def get_response_from_db(user_message):
    # Normalize user message (e.g., "msc cs syllabus" → "msc_cs_syllabus")
    cleaned_message = user_message.lower().strip()
    cleaned_message = re.sub(r'\s+', '_', cleaned_message)

    # Connect to SQLite and query
    conn = sqlite3.connect('cs_department.db')
    cursor = conn.cursor()

    cursor.execute("SELECT response FROM responses WHERE intent LIKE ?", ('%' + cleaned_message + '%',))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return "Sorry, I don't understand that yet."

@app.route('/', methods=['POST'])
def telegram_webhook():
    data = request.json

    if 'message' in data and 'text' in data['message']:
        chat_id = data['message']['chat']['id']
        user_message = data['message']['text']

        bot_response = get_response_from_db(user_message)

        # Send response back to user
        requests.post(TELEGRAM_API_URL, json={
            'chat_id': chat_id,
            'text': bot_response
        })

    return 'ok', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
