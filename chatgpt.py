import requests
import json
import os
from dotenv import load_dotenv

load_dotenv() 
openai_api_key = os.getenv("OPEN_AI_KEY")
if openai_api_key is None:
    raise ValueError(
        "OpenAI API key is not set. Define OPEN_AI_KEY in your environment or in a local .env file."
    )

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print(response.json()['choices'][0]['message']['content'])
else:
    print("Error:", response.status_code, response.text)