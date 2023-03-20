import openai
from typing import Dict, List, Tuple
from handlers.dbhandler import store_embedding_in_db, get_embeddings_from_db
import numpy as np
from openai.embeddings_utils import get_embedding, cosine_similarity
#from handlers.embeddinghandler import embed_text, find_similar_text, store_embedding, get_embeddings
import logging
import pandas as pd
from datetime import datetime
import handlers.file_dbaccess as file_dbaccess


logging.basicConfig(level=logging.DEBUG)

db = file_dbaccess.LocalFileDbAccess("embedded_1k_reviews.csv")

'''
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    logging.debug(f"Getting embedding for text: {text}")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']
'''
'''
def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
'''
def embed_text(text):
    logging.debug(f"Embedding text: {text}")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    text_embedding = get_embedding(text, engine='text-embedding-ada-002')

    df = db.get()

    df = df.append({"time":dt_string,"message":text, "ada_search": text_embedding},ignore_index=True)
    db.save(df)
    return "embedding done"
'''
def search_rembeds(df, text, n=3, pprint=True):
   embedding = get_embedding(text, model='text-embedding-ada-002')
   df['similarities'] = df.ada_embedding.apply(lambda x: cosine_similarity(x, embedding))
   res = df.sort_values('similarities', ascending=False).head(n)
   if pprint:
        for r in res:
            print(r[:200])
            print()
   return res
'''

def construct_prompt(question, df, top_n=3):
    # Get the context
    context = generate_context(question, df, top_n)
    header =  header = """Answer the question in details, based only on the provided context and nothing else, and if the answer is not contained within the text below, say "I don't know.", do not invent or deduce!\n\nContext:\n"""
    return header + "".join(context) + "Q: " + question + "\n A:"

def generate_context(question, df, top_n=3):
    most_similiar = return_most_similiar(question, df, top_n)
    # Get the top 3 most similar messages
    top_messages = most_similiar["message"].values
    # Concatenate the top 3 messages into a single string
    context = '\n '.join(top_messages)
    return context

def return_most_similiar(question, df, top_n=3):
    # Get the embedding for the question
    question_embedding = get_embedding(question, engine='text-embedding-ada-002')
    # Get the embedding for the messages in the database
    df["ada_search"] = df["ada_search"].apply(eval).apply(np.array)
    # Get the similarity between the question and the messages in the database
    df['similarity'] = df.ada_search.apply(lambda x: cosine_similarity(x, question_embedding))
    # Get the index of the top 3 most similar message
    most_similiar = df.sort_values('similarity', ascending=False).head(top_n)
    return most_similiar


def find_similar_text(query, embeddings=None):
    logging.debug(f"Finding similar text for query: {query}")
    df = pd.read_csv('embedded_1k_reviews.csv')
    res = return_most_similiar(query, df, top_n=1) #need to be configurable
    msg_reply = ''
    for i in range(len(res)):
            msg_reply += res.iloc[i]['time'] + ': ' + res.iloc[i]['message'] + '\n'
    return msg_reply

'''  
def store_embedding(user_phone: str, text: str, embedding: List[float]) -> None:
    embedding_array = np.array(embedding)
    embedding_str = np.array2string(embedding_array, separator=',', max_line_width=np.inf, formatter={'float_kind': '{:.17f}'.format})
    embedding_str = embedding_str.replace(" ", "")  # Remove spaces
    store_embedding_in_db(user_phone, text, embedding_str)
'''
def store_embedding(user_phone: str, text: str, embedding: List[float]) -> None:
    embedding_array = np.array(embedding)
    embedding_binary = embedding_array.tobytes()
    store_embedding_in_db(user_phone, text, embedding_binary)



def get_embeddings(user_phone: str) -> Dict[str, np.ndarray]:
    #embeddings_data = get_embeddings_from_db(user_phone)
    #embeddings = {text: np.frombuffer(embedding_bytes) for text, embedding_bytes in embeddings_data}
    return None#embeddings

'''
def get_embeddings(user_phone: str) -> Dict[str, np.ndarray]:
    embeddings_data = get_embeddings_from_db(user_phone)
    embeddings = {}
    for item in embeddings_data:
        text = item['text']
        embedding_str = item['embedding']
        embedding_array = np.fromstring(embedding_str, sep=',')
        print(f"Text: {text}")
        print(f"Embedding string: {embedding_str}")
        print(f"Embedding array: {embedding_array}")
        embeddings[text] = embedding_array
    return embeddings
'''
'''
def get_embeddings(user_phone: str) -> Dict[str, np.ndarray]:
    embeddings_data = get_embeddings_from_db(user_phone)
    print(embeddings_data) 
    embeddings = {}
    for text, embedding_str in embeddings_data:
        emb = np.fromstring(embedding_str, sep=',')
        if emb.shape[0] == 0:
            logging.warning(f"Empty embedding found for text: '{text}'")
        else:
            embeddings[text] = emb
            logging.info(f"Loaded embedding for text: '{text}', embedding: {emb}")
    return embeddings
'''
