import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def handle_img(img_prompt):
    image_response = openai.Image.create(
        prompt=img_prompt,
        n=2,
        size="1024x1024"
    )

    # Assuming you want the first image's URL
    image_url = image_response['data'][0]['url']
    return image_url
