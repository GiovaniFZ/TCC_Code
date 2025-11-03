import requests
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()
start_time = time.time()

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
    "model": "gpt-4.1-mini",
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
end_time = time.time()
elapsed_time = end_time - start_time

if response.status_code == 200:
    content = response.json()['choices'][0]['message']['content']
    print('Answer content:', content)
    print('Tokens used:', response.json()['usage']['total_tokens'])
    print(f"Elapsed time: {elapsed_time} seconds")
else:
    print("Error:", response.status_code, response.text)