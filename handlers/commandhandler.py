# Add this import at the beginning of the file
from handlers.confighandler import config
from handlers.embeddinghandler import embed_text, find_similar_text, store_embedding as store_embedding, get_embeddings as get_embeddings



# Update the handle_command function as follows
def handle_command(user_phone: str, command: str) -> str:
    if command.lower().startswith("/remember "):
        text_to_remember = command[10:]
        embedding = embed_text(text_to_remember)
        store_embedding(user_phone, text_to_remember, embedding)
        return "I've remembered your message."
      
    elif command.lower().startswith("/recall"):
        query = command[7:].strip()
        embeddings = get_embeddings(user_phone)
        return find_similar_text("Find me a text that is similar to this one. "+query, embeddings)
      
    elif command.lower().startswith("/config "):
        config_parts = command[8:].split()
        persistent = False
        if "/persistent" in config_parts:
            config_parts.remove("/persistent")
            persistent = True
        config_line = " ".join(config_parts)
        key_value = config_line.split("=")
        if len(key_value) == 2:
            key, value = key_value[0].strip(), key_value[1].strip()
            return config.update_config(key, value, persistent)
        else:
            return "Invalid config command format. Please use /config KEY=VALUE or /config /persistent KEY=VALUE."
    else:
        return "Invalid command. Please use /remember, /recall, or /config."
