from google import genai
from dotenv import load_dotenv
import os
import time

def save_txt(folder_name, nome_arquivo, conteudo):
    os.makedirs(folder_name, exist_ok=True)
    where = os.path.join(folder_name, nome_arquivo)
    with open(where, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client()

questions = ["Crie um código em python que leia um arquivo de texto e conte o número de linhas e palavras.",
             "Crie uma função em TypeScript que valide emails e números de telefone utilizando expressões regulares (regex).",
             "Mostre como configurar a conexão com um banco de dados usando Sequelize em JavaScript.",
             "Crie um código em Python que leia um arquivo CSV e envie os dados para uma API via requisição HTTP.",
             "Crie um middleware de autenticação JWT completo em Node.js (gerar token, verificar e renovar).",
             "Crie uma API REST em Node.js com Express que permita cadastrar, listar e deletar produtos, utilizando Sequelize e MySQL."
             ]

for i in range(len(questions)):
    start_time = time.time()
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=questions[i],
)
    token_count = response.usage_metadata.total_token_count
    end_time = time.time()
    elapsed_time = end_time - start_time
    response_full = response.text + f"\n\nTime taken: {elapsed_time} seconds\nTokens used: {token_count}"
    save_txt("../responses/code_generation", f"response_gemini_{i+1}.md", response_full)

print("All responses saved to text files.")