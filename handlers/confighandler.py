import os



class ConfigHandler:
    def __init__(self, from_number=None, to_number=None):
        config_from_db = None
        if from_number and to_number:
            from handlers.dbhandler import load_config_from_db, save_config_to_db
            config_from_db = load_config_from_db(from_number, to_number)


        self.PROMPTLAYER_API_KEY = config_from_db.get('PROMPTLAYER_API_KEY', os.environ['PROMPTLAYER_API_KEY']) if config_from_db else os.environ['PROMPTLAYER_API_KEY']
        self.OPENAI_API_KEY = config_from_db.get('OPENAI_API_KEY', os.environ['OPENAI_API_KEY']) if config_from_db else os.environ['OPENAI_API_KEY']
        self.OPENAI_API_MODEL = config_from_db.get('OPENAI_API_MODEL', os.environ['OPENAI_API_MODEL']) if config_from_db else os.environ['OPENAI_API_MODEL']
        self.INITIAL_PROMPT = config_from_db.get('INITIAL_PROMPT', os.environ['INITIAL_PROMPT']) if config_from_db else os.environ['INITIAL_PROMPT']
        self.TWILIO_PHONE_NUMBER = config_from_db.get('TWILIO_PHONE_NUMBER', os.environ['TWILIO_PHONE_NUMBER']) if config_from_db else os.environ['TWILIO_PHONE_NUMBER']
        self.DB_TYPE = config_from_db.get('DB_TYPE', os.environ['DB_TYPE']) if config_from_db else os.environ['DB_TYPE']
        self.DB_USER = config_from_db.get('DB_USER', os.environ.get('DB_USER')) if config_from_db else os.environ.get('DB_USER')
        self.DB_PASSWORD = config_from_db.get('DB_PASSWORD', os.environ.get('DB_PASSWORD')) if config_from_db else os.environ.get('DB_PASSWORD')
        self.DB_HOST = config_from_db.get('DB_HOST', os.environ.get('DB_HOST')) if config_from_db else os.environ.get('DB_HOST')
        self.DB_NAME = config_from_db.get('DB_NAME', os.environ.get('DB_NAME')) if config_from_db else os.environ.get('DB_NAME')
        self.DB_PORT = config_from_db.get('DB_PORT', os.environ.get('DB_PORT')) if config_from_db else os.environ.get('DB_PORT')
        self.DB_PATH = config_from_db.get('DB_PATH', os.environ.get('DB_PATH')) if config_from_db else os.environ.get('DB_PATH')

def update_config(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
            return f"Config '{key}' has been updated to '{value}'."
        else:
            return f"Invalid config key '{key}'."
          
def update_config(self, key, value, persistent=False):
        if hasattr(self, key):
            setattr(self, key, value)
            if persistent:
                save_config_to_db(key, value)
            return f"Config '{key}' has been updated to '{value}'."
        else:
            return f"Invalid config key '{key}'."

          
config = ConfigHandler()
