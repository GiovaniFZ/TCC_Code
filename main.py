from google import genai
from dotenv import load_dotenv
import os

load_dotenv() 

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the capital of France?",
)

print(response.text)