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
    return json.dumps(message)

def deserialize_message(message_json):
    return json.loads(message_json)

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
            messages = [deserialize_message(message_json) for message_json in db[key]]
        else:
            messages = []
    else:
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT Role, Message FROM chat WHERE `From` = '{phone_number}' OR `To` = '{phone_number}' ORDER BY DateTime ASC;")
        messages = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]

        cursor.close()
        connection.close()

    return messages

def insert_message_to_db(from_number, to_number, role, message):
    if db_type == 'replit':
        key = format_key(from_number)
        message_json = serialize_message({"role": role, "content": message, "timestamp": datetime.now().isoformat()})

        if key in db:
            db[key] = db[key] + [message_json]
        else:
            db[key] = [message_json]
    else:
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO chat (DateTime, `From`, `To`, Role, Message) VALUES (NOW(), %s, %s, %s, %s);",
                       (from_number, to_number, role, message))
        connection.commit()

        cursor.close()
        connection.close()
