import requests
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()
start_time = time.time()
openai_api_key = os.getenv("OPEN_AI_KEY")


def save_txt(folder_name, nome_arquivo, conteudo):
    os.makedirs(folder_name, exist_ok=True)
    where = os.path.join(folder_name, nome_arquivo)
    with open(where, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)


questions = ["Crie um código em python que leia um arquivo de texto e conte o número de linhas e palavras.",
             "Crie uma função em TypeScript que valide emails e números de telefone utilizando expressões regulares (regex).",
             "Mostre como configurar a conexão com um banco de dados usando Sequelize em JavaScript.",
             "Crie um código em Python que leia um arquivo CSV e envie os dados para uma API via requisição HTTP.",
             "Crie um middleware de autenticação JWT completo em Node.js (gerar token, verificar e renovar).",
             "Crie uma API REST em Node.js com Express que permita cadastrar, listar e deletar produtos, utilizando Sequelize e MySQL."
             ]

if openai_api_key is None:
    raise ValueError(
        "OpenAI API key is not set. Define OPEN_AI_KEY in your environment or in a local .env file."
    )

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}


for i in range(len(questions)):
    start_time = time.time()
    data = {
        "model": "gpt-4.1-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": questions[i]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        tokens_count = response.json()['usage']['total_tokens']
        content = response.json()['choices'][0]['message']['content']
        end_time = time.time()
        elapsed_time = end_time - start_time
        save_txt("../responses/code_generation", f"response_chatgpt_{i+1}.txt", content + f"\n\nTime taken: {elapsed_time} seconds\nTokens used: {tokens_count}")
    else:
        print("Error:", response.status_code, response.text)
        
print("All responses saved to text files.")