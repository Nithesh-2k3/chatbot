from flask import Flask, request
import sqlite3
import requests

# Your Telegram bot token
BOT_TOKEN = '7629694750:AAG6vET2cga29hi14V-9lh13ZJEPWSAkjDs'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

# Initialize Flask app
app = Flask(__name__)

# Database function to fetch answers
def get_response_from_db(user_message):
    conn = sqlite3.connect('cs_department.db')
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM chatbot WHERE question LIKE ?", ('%' + user_message + '%',))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "Sorry, I don't have an answer for that."

# Flask route to handle Telegram updates
@app.route('/', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if 'message' in data and 'text' in data['message']:
        chat_id = data['message']['chat']['id']
        user_message = data['message']['text']

        # Get answer from database
        bot_response = get_response_from_db(user_message)

        # Send response back to Telegram
        payload = {
            'chat_id': chat_id,
            'text': bot_response
        }
        requests.post(TELEGRAM_API_URL, json=payload)

    return 'ok'

# Run the app (Render uses port 10000+, so we bind to 0.0.0.0)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
