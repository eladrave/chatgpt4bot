import os
import json
from datetime import datetime
import mysql.connector
import psycopg2
from replit import db

db_type = os.environ['DB_TYPE']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
db_port = os.environ['DB_PORT']

# Additional helper functions for Replit DB

def format_key(phone_number):
    return f"chat_{phone_number}"

def serialize_message(message):
    return {
        "role": message["role"],
        "content": message["content"]
    }

def deserialize_message(message_json):
    message = json.loads(message_json)
    return {
        "role": message["role"],
        "content": message["content"]
    }

  
# Updated functions

def get_database_connection():
    if db_type == 'mysql':
        return mysql.connector.connect(
            user=db_user, password=db_password, host=db_host, database=db_name, port=db_port
        )
    elif db_type == 'postgres':
        return psycopg2.connect(
            user=db_user, password=db_password, host=db_host, dbname=db_name, port=db_port
        )
    elif db_type == 'replit':
        return None
    else:
        raise ValueError("Invalid database type. Please set the 'DB_TYPE' environment variable to 'mysql', 'postgres', or 'replit'.")

def get_messages_from_db(phone_number):
    if db_type == 'replit':
        key = format_key(phone_number)
        if key in db:
            messages = []
            for message in db[key]:
                if isinstance(message, str):
                    messages.append(json.loads(message))
                elif isinstance(message, dict):
                    messages.append(dict(message))
            return messages
        else:
            return []
    else:
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT `From`, `To`, Role, Message FROM chat WHERE `From`=%s OR `To`=%s ORDER BY DateTime;",
                       (phone_number, phone_number))
        result = cursor.fetchall()

        messages = [{"role": row[2], "content": row[3]} for row in result]

        cursor.close()
        connection.close()

        return messages


def insert_message_to_db(from_number, to_number, role, message):
    if db_type == 'replit':
        key = format_key(from_number)
        message_obj = {"role": role, "content": message, "timestamp": datetime.now().isoformat()}

        if key in db:
            messages = db[key]
            messages.append(message_obj)
            db[key] = messages
        else:
            db[key] = [message_obj]
    else:
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO chat (DateTime, `From`, `To`, Role, Message) VALUES (NOW(), %s, %s, %s, %s);",
                       (from_number, to_number, role, message))
        connection.commit()

        cursor.close()
        connection.close()

