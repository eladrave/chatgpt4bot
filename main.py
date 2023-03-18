import openai
import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from dbhandler import get_messages_from_db, insert_message_to_db
import promptlayer

promptlayer.api_key = os.environ['PROMPTLAYER_API_KEY']
openai = promptlayer.openai

load_dotenv()
app = Flask(__name__)
app.debug = True

openai.api_key = os.environ['OPENAI_API_KEY']
model = os.environ['OPENAI_API_MODEL']
initial_prompt = os.environ['INITIAL_PROMPT']
twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']


@app.route('/wachat', methods=['POST'])
def wachat():
  user_phone = request.form.get('From')
  user_name = request.form.get('ProfileName')
  user_message = request.form.get('Body')

  messages = get_messages_from_db(user_phone)
  if not len(messages):
    messages = [{"role": "system", "content": initial_prompt}]

  # Remove the 'timestamp' field from messages before sending to the API
  for message in messages:
    message.pop('timestamp', None)
  insert_message_to_db(user_phone, twilio_phone_number, "user", user_message)

  messages = [{k: v for k, v in msg.items()} for msg in messages]

  response = openai.ChatCompletion.create(model=model, messages=messages)

  assistant_message = response.choices[0].message.content
  insert_message_to_db(twilio_phone_number, user_phone, "assistant",
                       assistant_message)

  twilio_response = MessagingResponse()
  twilio_response.message(assistant_message)

  return str(twilio_response)


if __name__ == '__main__':
  app.run("0.0.0.0")
