import os
import json
from datetime import datetime
import mysql.connector
import psycopg2
import sqlite3
from handlers.confighandler import config

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

    if db_type == 'sqlite':
      cursor.execute(
        "SELECT `From`, `To`, Role, Message FROM chat WHERE `From`=? OR `To`=? ORDER BY DateTime;",
        (phone_number, phone_number))
    else:
      cursor.execute(
        "SELECT `From`, `To`, Role, Message FROM chat WHERE `From`=%s OR `To`=%s ORDER BY DateTime;",
        (phone_number, phone_number))

    result = cursor.fetchall()

    messages = [{"role": row[2], "content": row[3]} for row in result]

    cursor.close()
    connection.close()

    return messages


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
