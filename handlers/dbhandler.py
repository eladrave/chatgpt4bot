import os
import json
from datetime import datetime
import mysql.connector
import psycopg2
import sqlite3
from handlers.confighandler import config
from typing import Dict, List
import numpy as np


db_type = config.DB_TYPE
db_user = config.DB_USER
db_password = config.DB_PASSWORD
db_host = config.DB_HOST
db_name = config.DB_NAME
db_port = config.DB_PORT
db_path = config.DB_PATH


def format_key(phone_number):
  return f"chat_{phone_number}"


def serialize_message(message):
  return {"role": message["role"], "content": message["content"]}


def deserialize_message(message_json):
  message = json.loads(message_json)
  return {"role": message["role"], "content": message["content"]}


def get_database_connection():
  if db_type == 'mysql':
    return mysql.connector.connect(user=db_user,
                                   password=db_password,
                                   host=db_host,
                                   database=db_name,
                                   port=db_port)
  elif db_type == 'postgres':
    return psycopg2.connect(user=db_user,
                            password=db_password,
                            host=db_host,
                            dbname=db_name,
                            port=db_port)
  elif db_type == 'sqlite':
    return sqlite3.connect(db_path)
  else:
    raise ValueError(
      "Invalid database type. Please set the 'DB_TYPE' environment variable to 'mysql', 'postgres', 'sqlite', or 'replit'."
    )


def get_messages_from_db(phone_number):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT text, embedding FROM embeddings WHERE user_phone = ?", (phone_number,)
    )

    # Retrieve the embeddings as numpy arrays
    embeddings = [
        (text, np.frombuffer(embedding_binary, dtype=np.float64))
        for text, embedding_binary in cursor.fetchall()
    ]

    connection.close()
    return embeddings


def insert_message_to_db(from_number, to_number, role, message):
  
    connection = get_database_connection()
    cursor = connection.cursor()

    if db_type == 'sqlite':
      cursor.execute(
        "INSERT INTO chat (DateTime, `From`, `To`, Role, Message) VALUES (datetime('now'), ?, ?, ?, ?);",
        (from_number, to_number, role, message))
    else:
      cursor.execute(
        "INSERT INTO chat (DateTime, `From`, `To`, Role, Message) VALUES (NOW(), %s, %s, %s, %s);",
        (from_number, to_number, role, message))

    connection.commit()

    cursor.close()
    connection.close()



def load_config_from_db(from_number, to_number):
    connection = get_database_connection()
    cursor = connection.cursor()

    if db_type == 'sqlite':
        cursor.execute(
            "SELECT ConfigKey, ConfigValue FROM config WHERE `From`=? AND `To`=?;",
            (from_number, to_number))
    else:
        cursor.execute(
            "SELECT ConfigKey, ConfigValue FROM config WHERE `From`=%s AND `To`=%s;",
            (from_number, to_number))

    result = cursor.fetchall()
    config_dict = {row[0]: row[1] for row in result}

    cursor.close()
    connection.close()

    return config_dict

def store_embedding_in_db(user_phone: str, text: str, embedding: List[float]) -> None:
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    embedding_array = np.array(embedding)  # Convert the list to a NumPy array
    embedding_binary = embedding_array.tobytes()  # Call 'tobytes' on the NumPy array

    cursor.execute(
        "INSERT INTO embeddings (user_phone, text, embedding) VALUES (?, ?, ?)",
        (user_phone, text, embedding_binary),
    )

    conn.commit()
    conn.close()

    print(f"Stored embedding for '{text}' in the database")

def get_embeddings_from_db(user_phone: str) -> List[Dict[str, float]]:
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT text, embedding FROM embeddings WHERE user_phone = ?", (user_phone,)
    )

    fetched_data = cursor.fetchall()
    print("Fetched data from DB:", fetched_data)

    embeddings = [
        {"text": text, "embedding": np.frombuffer(embedding_binary, dtype=np.float64)}
        for text, embedding_binary in fetched_data
    ]
    print(embeddings)
    conn.close()
    return embeddings

def save_config_to_db(key: str, value: str) -> None:
    conn = get_database_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
        (key, value)
    )
    
    conn.commit()
    cursor.close()
    conn.close()