from google import genai
from dotenv import load_dotenv
import os
import time

def save_txt(folder_name, nome_arquivo, conteudo):
    os.makedirs(folder_name, exist_ok=True)
    where = os.path.join(folder_name, nome_arquivo)
    with open(where, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)
        
def open_txt(name_file):
    with open(f"{name_file}.txt", "r", encoding="utf-8") as arquivo:
        return arquivo.read()

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client()

for i in range(6):
    question = open_txt(f"../../prompts/code_comprehension/prompt{i+1}")
    start_time = time.time()
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=question,
)
    token_count = response.usage_metadata.total_token_count
    end_time = time.time()
    elapsed_time = end_time - start_time
    response_full = response.text + f"\n\nTime taken: {elapsed_time} seconds\nTokens used: {token_count}"
    save_txt("../responses/code_comprehension", f"response_gemini_{i+1}.txt", response_full)

print("All responses saved to text files.")