from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv() 

start_time = time.time()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client()

questions = ["Crie um código em python que leia um arquivo de texto e conte o número de linhas e palavras.",
             "Crie uma função em TypeScript que valide emails e números de telefone utilizando expressões regulares (regex).",
             "Mostre como configurar a conexão com um banco de dados usando Sequelize em JavaScript.",
             "Crie um código em Python que leia um arquivo CSV e envie os dados para uma API via requisição HTTP.",
             "Crie um middleware de autenticação JWT completo em Node.js (gerar token, verificar e renovar).",
             "Crie uma API REST em Node.js com Express que permita cadastrar, listar e deletar produtos, utilizando Sequelize e MySQL."
             ]

answers = []
tokens = []

for i in range(len(questions)):
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=questions[i],
)
    answers.append(response.text)
    tokens.append(response.usage_metadata.total_token_count)


end_time = time.time()
elapsed_time = end_time - start_time

print('Responses:', answers)
print('Tokens used:', tokens)
print(f"Elapsed time: {elapsed_time} seconds")