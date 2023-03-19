import os

class ConfigHandler:
    def __init__(self):
        self.PROMPTLAYER_API_KEY = os.environ['PROMPTLAYER_API_KEY']
        self.OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
        self.OPENAI_API_MODEL = os.environ['OPENAI_API_MODEL']
        self.INITIAL_PROMPT = os.environ['INITIAL_PROMPT']
        self.TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
        self.DB_TYPE = os.environ['DB_TYPE']
        self.DB_USER = os.environ.get('DB_USER')
        self.DB_PASSWORD = os.environ.get('DB_PASSWORD')
        self.DB_HOST = os.environ.get('DB_HOST')
        self.DB_NAME = os.environ.get('DB_NAME')
        self.DB_PORT = os.environ.get('DB_PORT')
        self.DB_PATH = os.environ.get('DB_PATH')

config = ConfigHandler()
