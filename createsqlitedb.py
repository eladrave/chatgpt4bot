import sqlite3
import os
from handlers.confighandler import config

# Create the database and connection
connection = sqlite3.connect(config.DB_PATH)

# Create a table for storing data
connection.execute("CREATE TABLE chat (DateTime DATETIME NOT NULL, `From` TEXT NOT NULL, `To` TEXT NOT NULL, Role TEXT NOT NULL, Message TEXT NOT NULL)")
