import os
import handlers.dbhandler as dbhandler
import numpy as np


def clear_database():
  if dbhandler.db_type == 'replit':
    keys_to_delete = []

    # Collect all the keys to delete
    for key in dbhandler.db.keys():
      keys_to_delete.append(key)

    # Delete keys
    for key in keys_to_delete:
      del dbhandler.db[key]

    print("Replit DB has been cleared.")
  else:
    connection = dbhandler.get_database_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM chat;")

    connection.commit()
    cursor.close()
    connection.close()

    print("Database has been cleared.")


def display_database():
  if dbhandler.db_type == 'replit':
    print("Replit DB contents:")
    for key in dbhandler.db.keys():
      print(f"{key}: {dbhandler.db[key]}")
  else:
    connection = dbhandler.get_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM chat;")
    result = cursor.fetchall()

    print("Database contents:")
    for row in result:
      print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}")

    #cursor.close()

    cursor.execute("SELECT * FROM embeddings;")
    result = cursor.fetchall()

    print("Database contents:")
    for row in result:
      print(f"{row[0]}, {row[1]}")

    cursor.close()
    connection.close()

def display_embeddings():
    connection = dbhandler.get_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT user_phone, text, embedding FROM embeddings")
    results = cursor.fetchall()

    for phone, text, embedding_str in results:
        embedding = np.fromstring(embedding_str, sep=',')
        print(f"Phone: {phone}, Text: {text}, Embedding: {embedding}")

    connection.close()

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(description="Database Manager")
  parser.add_argument('--clear',
                      action='store_true',
                      help="Clear the database")
  parser.add_argument('--display',
                      action='store_true',
                      help="Display the database contents")
  parser.add_argument('--embedding',
                      action='store_true',
                      help="Display the embedding contents")

  args = parser.parse_args()

  if args.clear:
    clear_database()
  elif args.display:
    display_database()
  elif args.embedding:
    display_embeddings()
  else:
    parser.print_help()
