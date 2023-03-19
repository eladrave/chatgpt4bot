import sqlite3
import os
from handlers.confighandler import config

# Create the database and connection
connection = sqlite3.connect(config.DB_PATH)

# Create a table for storing data

connection.execute("CREATE TABLE IF NOT EXISTS chat (DateTime DATETIME NOT NULL, `From` TEXT NOT NULL, `To` TEXT NOT NULL, Role TEXT NOT NULL, Message TEXT NOT NULL)")

connection.execute("CREATE TABLE IF NOT EXISTS config (id INTEGER PRIMARY KEY AUTOINCREMENT, `From` TEXT NOT NULL, `To` TEXT NOT NULL, ConfigKey TEXT NOT NULL, ConfigValue TEXT NOT NULL)")

#connection.execute("CREATE TABLE IF NOT EXISTS config(key TEXT PRIMARY KEY,value TEXT NOT NULL)")

connection.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY,
        user_phone TEXT NOT NULL,
        text TEXT NOT NULL,
        embedding TEXT NOT NULL
    )
""")
