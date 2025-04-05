import sqlite3
from difflib import get_close_matches

def get_response_from_db(user_message):
    conn = sqlite3.connect('cs_department.db')
    cursor = conn.cursor()

    cursor.execute("SELECT intent, response FROM responses")
    data = cursor.fetchall()

    intents = [row[0] for row in data]
    matches = get_close_matches(user_message.lower(), intents, n=1, cutoff=0.4)

    if matches:
        matched_intent = matches[0]
        for intent, response in data:
            if intent == matched_intent:
                conn.close()
                return response
    conn.close()
    return "Sorry, I don't understand that yet."
