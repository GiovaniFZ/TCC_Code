from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv() 

start_time = time.time()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the capital of France?",
)

end_time = time.time()
elapsed_time = end_time - start_time

print('Response:', response.text)
print('Tokens used:', response.usage_metadata.total_token_count)
print(f"Elapsed time: {elapsed_time} seconds")