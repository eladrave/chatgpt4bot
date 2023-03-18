import openai
import os
import sys
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()
app = Flask(__name__)

openai.api_key = os.environ['OPENAI_API_KEY']
model = os.environ['OPENAI_API_MODEL']
initial_prompt = os.environ['INITIAL_PROMPT']
twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']

db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']

def get_database_connection():
    return mysql.connector.connect(
        user=db_user, password=db_password, host=db_host, database=db_name
    )

def get_messages_from_db(phone_number):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(f"SELECT Role, Message FROM chat WHERE `From` = '{phone_number}' OR `To` = '{phone_number}' ORDER BY DateTime ASC;")
    messages = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return messages

def insert_message_to_db(from_number, to_number, role, message):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO chat (DateTime, `From`, `To`, Role, Message) VALUES (NOW(), %s, %s, %s, %s);",
                   (from_number, to_number, role, message))
    connection.commit()

    cursor.close()
    connection.close()

@app.route('/wachat', methods=['POST'])
def wachat():
    user_phone = request.form.get('From')
    user_name = request.form.get('ProfileName')
    user_message = request.form.get('Body')

    insert_message_to_db(user_phone, twilio_phone_number, "user", user_message)

    messages = get_messages_from_db(user_phone)
    if not messages:
        messages = [
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": ""},
            {"role": "assistant", "content": ""}
        ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    assistant_message = response.choices[0].message.content
    insert_message_to_db(twilio_phone_number, user_phone, "assistant", assistant_message)

    twilio_response = MessagingResponse()
    twilio_response.message(assistant_message)

    return str(twilio_response)

if __name__ == '__main__':
    app.run()
