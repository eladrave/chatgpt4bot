import openai
import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from handlers.dbhandler import get_messages_from_db, insert_message_to_db
import promptlayer
import requests
import io
import tempfile
from typing import Tuple
import soundfile as sf
import logging
from handlers.imagehandler import handle_img
from handlers.confighandler import config
from handlers.embeddinghandler import embed_text, find_similar_text, store_embedding, get_embeddings
from handlers.commandhandler import handle_command




logging.basicConfig(level=logging.INFO)

promptlayer.api_key = config.PROMPTLAYER_API_KEY #os.environ['PROMPTLAYER_API_KEY']
#openai = promptlayer.openai

load_dotenv()
app = Flask(__name__)
app.debug = True

openai.api_key = config.OPENAI_API_KEY
model = config.OPENAI_API_MODEL
initial_prompt = config.INITIAL_PROMPT
twilio_phone_number = config.TWILIO_PHONE_NUMBER

'''
openai.api_key = os.environ['OPENAI_API_KEY']
model = os.environ['OPENAI_API_MODEL']
initial_prompt = os.environ['INITIAL_PROMPT']
twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']
'''

def download_media(url: str) -> Tuple[str, io.BytesIO]:
  response = requests.get(url)
  response.raise_for_status()
  content_disposition = response.headers.get('Content-Disposition', 'unknown')
  file_name = content_disposition.split("filename=")[-1].strip(
    '"') if "filename=" in content_disposition else "unknown"
  content = io.BytesIO(response.content)
  return (file_name, content)


def handle_audio(url: str) -> str:
  filename, audio_file = download_media(url)

  with tempfile.NamedTemporaryFile(
      delete=False, suffix=f".{filename.split('.')[-1]}") as temp_audio_file:
    temp_audio_file.write(audio_file.read())
    temp_audio_file.flush()

    data, samplerate = sf.read(temp_audio_file.name)
    with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=".wav") as temp_wav_file:
      sf.write(temp_wav_file.name,
               data,
               samplerate,
               format='WAV',
               subtype='PCM_16')
      with open(temp_wav_file.name, 'rb') as wav_file:
        response = openai.Audio.transcribe("whisper-1", wav_file)

    os.unlink(temp_wav_file.name)
  os.unlink(temp_audio_file.name)

  print(response)
  transcript = response['text']
  return transcript


def handle_image(url: str):
  # Add your implementation to handle images
  pass


def handle_document(url: str):
  # Add your implementation to handle documents
  pass


def process_openai_response(response_text):
  img_start = response_text.find("[img: ")
  if img_start != -1:
    img_end = response_text.find("]", img_start)
    if img_end != -1:
      img_value_start = response_text.find('"', img_start) + 1
      img_value_end = response_text.find('"', img_value_start)
      img_prompt = response_text[img_value_start:img_value_end]
      oai_response = response_text[:img_start].strip()

      image_url = handle_img(img_prompt)
      return oai_response, image_url
  return response_text, None


@app.route('/wachat', methods=['POST'])
def wachat():
    user_phone = request.form.get('From')
    user_name = request.form.get('ProfileName')
    user_message = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    media_type = request.form.get('MediaContentType0')
    whatsapp_number = request.form.get('To')

    image_url = None
    messages = []

    if media_url:
        if media_type.startswith('audio'):
            user_message = handle_audio(media_url)
        elif media_type.startswith('image'):
            handle_image(media_url)
        elif media_type.startswith('application'):
            handle_document(media_url)

    if user_message.startswith("/"):
        oai_response = handle_command(user_phone, user_message)
    else:
        messages = get_messages_from_db(user_phone)
        logging.info(f"Messages from DB: {messages}")

        if not len(messages):
            messages = [{"role": "system", "content": initial_prompt}]
            insert_message_to_db(user_phone, twilio_phone_number, "system",
                                initial_prompt)

        # Remove the 'timestamp' field from messages before sending to the API
        for message in messages:
            message.pop('timestamp', None)
        insert_message_to_db(user_phone, twilio_phone_number, "user", user_message)

        messages.append({"role": "user", "content": user_message})

        logging.info(f"Messages after user input: {messages}")

        response = openai.ChatCompletion.create(model=model, messages=messages)

        assistant_message = response.choices[0].message.content
        oai_response, image_url = process_openai_response(assistant_message)

    twilio_response = MessagingResponse()

    if image_url is not None:
        twilio_response.message(oai_response).media(image_url)
    else:
        twilio_response.message(oai_response)

    insert_message_to_db(user_phone, twilio_phone_number, "assistant",
                            oai_response)
    messages.append({"role": "assistant", "content": oai_response})

    return str(twilio_response)


if __name__ == '__main__':
    app.run("0.0.0.0", port=8000)

