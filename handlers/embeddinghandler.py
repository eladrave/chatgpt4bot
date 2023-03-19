import openai
from typing import Dict, List, Tuple
from handlers.dbhandler import store_embedding_in_db, get_embeddings_from_db
import numpy as np
from openai.embeddings_utils import cosine_similarity
#from handlers.embeddinghandler import embed_text, find_similar_text, store_embedding, get_embeddings
import logging

logging.basicConfig(level=logging.DEBUG)


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    logging.debug(f"Getting embedding for text: {text}")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

def embed_text(text):
    logging.debug(f"Embedding text: {text}")
    embedding = get_embedding(text)
    return embedding

def find_similar_text(query, embeddings):
    logging.debug(f"Finding similar text for query: {query}")
    query_embedding = get_embedding(query)
    similarities = [(cosine_similarity(query_embedding, emb), text) for text, emb in embeddings.items()]
    sorted_similarities = sorted(similarities, key=lambda x: x[0], reverse=True)
    similar = sorted_similarities[0][1]
    logging.debug(f"Sorted_similarities: {similar}")
    return sorted_similarities[0][1] if sorted_similarities else None

  
def store_embedding(user_phone: str, text: str, embedding: List[float]) -> None:
    embedding_array = np.array(embedding)
    embedding_str = np.array2string(embedding_array, separator=',', max_line_width=np.inf)
    store_embedding_in_db(user_phone, text, embedding_str)


def get_embeddings(user_phone: str) -> Dict[str, np.ndarray]:
    embeddings_data = get_embeddings_from_db(user_phone)
    embeddings = {text: np.fromstring(embedding_str, sep=',') for text, embedding_str in embeddings_data}
    return embeddings
