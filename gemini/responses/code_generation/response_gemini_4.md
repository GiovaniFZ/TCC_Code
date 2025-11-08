Este código Python permite ler um arquivo CSV, iterar sobre suas linhas e enviar cada linha (ou um conjunto de linhas, se a API suportar batch) como um objeto JSON para uma API RESTful via requisições HTTP (POST, PUT ou PATCH).

**Pré-requisitos:**

Você precisará instalar a biblioteca `requests`, que facilita a realização de requisições HTTP em Python.
```bash
pip install requests
```

---

### Exemplo de Arquivo CSV (`dados.csv`)

Vamos criar um arquivo CSV de exemplo para testar:

```csv
id,nome,idade,cidade
1,João Silva,30,São Paulo
2,Maria Souza,25,Rio de Janeiro
3,Pedro Lima,35,Belo Horizonte
4,Ana Costa,28,Curitiba
```

---

### Código Python (`enviar_csv_para_api.py`)

```python
import csv
import requests
import json
import time

def send_csv_to_api(csv_file_path, api_url, http_method='POST', headers=None, batch_size=1, delay_between_requests=0.1):
    """
    Lê um arquivo CSV e envia seus dados para uma API via requisições HTTP.

    Args:
        csv_file_path (str): O caminho para o arquivo CSV.
        api_url (str): A URL do endpoint da API.
        http_method (str): O método HTTP a ser usado ('POST', 'PUT', 'PATCH'). Padrão é 'POST'.
        headers (dict, optional): Um dicionário de cabeçalhos HTTP adicionais (ex: para autenticação).
        batch_size (int): Quantidade de linhas para enviar em um único batch. Se 1, envia uma linha por vez.
                          Se > 1, agrupa linhas em uma lista e envia. A API deve suportar o formato de lista.
        delay_between_requests (float): Tempo em segundos para esperar entre as requisições (útil para evitar rate limiting).
    """

    if http_method.upper() not in ['POST', 'PUT', 'PATCH']:
        print(f"Método HTTP '{http_method}' não suportado. Use 'POST', 'PUT' ou 'PATCH'.")
        return

    processed_count = 0
    success_count = 0
    error_count = 0
    batch_data = []

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            # csv.DictReader lê cada linha como um dicionário onde as chaves são os nomes das colunas.
            reader = csv.DictReader(csvfile)

            print(f"Iniciando envio de dados do CSV '{csv_file_path}' para '{api_url}'...")

            for row in reader:
                processed_count += 1
                batch_data.append(row)

                # Se o batch_size for atingido ou se for a última linha
                if len(batch_data) == batch_size:
                    payload = batch_data if batch_size > 1 else batch_data[0] # Envia lista ou item único

                    try:
                        print(f"Enviando {'batch de' if batch_size > 1 else 'linha'} {processed_count - len(batch_data) + 1} a {processed_count}...")
                        
                        # Realiza a requisição HTTP
                        response = requests.request(http_method, api_url, json=payload, headers=headers)

                        if response.status_code in [200, 201, 202, 204]: # Códigos de sucesso comuns
                            success_count += 1
                            print(f"  Sucesso ({response.status_code}): {'Batch enviado.' if batch_size > 1 else f'Linha {processed_count} enviada.'}")
                            # Opcional: print(f"  Resposta da API: {response.json()}")
                        else:
                            error_count += 1
                            print(f"  Erro ({response.status_code}) ao enviar {'batch' if batch_size > 1 else f'linha {processed_count}'}:")
                            print(f"    Payload: {json.dumps(payload, indent=2)}")
                            print(f"    Resposta da API: {response.text}")

                    except requests.exceptions.RequestException as e:
                        error_count += 1
                        print(f"  Erro de conexão/requisição ao enviar {'batch' if batch_size > 1 else f'linha {processed_count}'}: {e}")
                        print(f"    Payload: {json.dumps(payload, indent=2)}")
                    finally:
                        batch_data = [] # Limpa o batch
                        time.sleep(delay_between_requests) # Espera antes da próxima requisição

            # Envia quaisquer itens restantes no batch, se houver
            if batch_data:
                payload = batch_data if batch_size > 1 else batch_data[0]
                try:
                    print(f"Enviando {'batch final de' if batch_size > 1 else 'última linha'} {processed_count - len(batch_data) + 1} a {processed_count}...")
                    response = requests.request(http_method, api_url, json=payload, headers=headers)
                    if response.status_code in [200, 201, 202, 204]:
                        success_count += 1
                        print(f"  Sucesso ({response.status_code}): {'Batch enviado.' if batch_size > 1 else f'Linha {processed_count} enviada.'}")
                    else:
                        error_count += 1
                        print(f"  Erro ({response.status_code}) ao enviar {'batch final' if batch_size > 1 else f'última linha {processed_count}'}:")
                        print(f"    Payload: {json.dumps(payload, indent=2)}")
                        print(f"    Resposta da API: {response.text}")
                except requests.exceptions.RequestException as e:
                    error_count += 1
                    print(f"  Erro de conexão/requisição ao enviar {'batch final' if batch_size > 1 else f'última linha {processed_count}'}: {e}")
                    print(f"    Payload: {json.dumps(payload, indent=2)}")
                finally:
                    time.sleep(delay_between_requests)

    except FileNotFoundError:
        print(f"Erro: O arquivo CSV '{csv_file_path}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

    print("\n--- Resumo do Envio ---")
    print(f"Total de linhas processadas no CSV: {processed_count}")
    print(f"Envios bem-sucedidos para a API: {success_count} {'(incluindo batches)' if batch_size > 1 else ''}")
    print(f"Envios com erro: {error_count}")
    print("------------------------")

if __name__ == "__main__":
    # --- Configurações ---
    CSV_FILE = 'dados.csv'
    API_URL = 'https://webhook.site/YOUR_WEBHOOK_URL_HERE' # Substitua pela sua URL da API real!
                                                          # Para testes, você pode usar um serviço como https://webhook.site/
                                                          # ou https://requestbin.com/ para ver as requisições chegando.
    HTTP_METHOD = 'POST' # 'POST' para criar, 'PUT' ou 'PATCH' para atualizar
    BATCH_SIZE = 1       # 1 para enviar uma linha por requisição, >1 para enviar um lote (se a API suportar)
    DELAY_SECONDS = 0.5  # Atraso em segundos entre as requisições

    # Exemplo de cabeçalhos (ex: para autenticação, tipo de conteúdo, etc.)
    # Descomente e preencha se sua API exigir.
    API_HEADERS = {
        'Content-Type': 'application/json',
        # 'Authorization': 'Bearer SEU_TOKEN_AQUI' 
        # 'X-API-KEY': 'SUA_CHAVE_DE_API_AQUI'
    }

    print("--- Iniciando Script de Envio de CSV para API ---")

    send_csv_to_api(
        csv_file_path=CSV_FILE,
        api_url=API_URL,
        http_method=HTTP_METHOD,
        headers=API_HEADERS,
        batch_size=BATCH_SIZE,
        delay_between_requests=DELAY_SECONDS
    )

    print("--- Script Concluído ---")
```

---

### Como usar:

1.  **Crie o arquivo `dados.csv`**: Salve o conteúdo do "Exemplo de Arquivo CSV" acima em um arquivo chamado `dados.csv` no mesmo diretório do seu script Python.
2.  **Obtenha uma URL de API de teste (opcional, mas recomendado)**: Vá para um site como [webhook.site](https://webhook.site/) ou [requestbin.com](https://requestbin.com/). Eles fornecem uma URL temporária onde você pode ver as requisições HTTP que chegam. Copie essa URL.
3.  **Atualize o código Python**:
    *   Substitua `'https://webhook.site/YOUR_WEBHOOK_URL_HERE'` pela URL da sua API real ou pela URL de teste que você obteve.
    *   Ajuste `HTTP_METHOD` se sua API espera um método diferente de `POST` (por exemplo, `PUT` se você estiver atualizando recursos existentes e seu CSV tiver uma coluna `id` que a API usa para identificar o recurso).
    *   Ajuste `BATCH_SIZE`: Se sua API suporta o envio de múltiplos registros em uma única requisição (geralmente uma lista de objetos JSON), você pode aumentar `BATCH_SIZE` para melhorar a performance. Se não tiver certeza, deixe em `1`.
    *   Ajuste `DELAY_SECONDS`: Para APIs com limites de taxa, um atraso entre as requisições pode ser crucial.
    *   **Importante**: Se sua API exige autenticação ou outros cabeçalhos, descomente e preencha o dicionário `API_HEADERS`.
4.  **Execute o script**:
    ```bash
    python enviar_csv_para_api.py
    ```

### Explicação do Código:

*   **`send_csv_to_api` função**: Encapsula toda a lógica de leitura e envio.
*   **`csv.DictReader`**: Esta é a melhor maneira de ler CSVs em Python, pois ele trata a primeira linha como cabeçalhos e permite acessar os dados de cada linha como um dicionário (ex: `row['nome']`).
*   **`requests.request(http_method, api_url, json=payload, headers=headers)`**: Esta é a parte central que faz a requisição HTTP.
    *   `http_method`: Permite que você especifique `POST`, `PUT`, `PATCH`, etc.
    *   `json=payload`: O `requests` automaticamente serializa seu dicionário Python (`payload`) para uma string JSON e define o cabeçalho `Content-Type` como `application/json`.
    *   `headers`: Um dicionário de cabeçalhos HTTP adicionais, útil para autenticação (`Authorization`), tipo de conteúdo (`Content-Type` para outros tipos que não JSON), etc.
*   **Tratamento de Erros**:
    *   `try...except FileNotFoundError`: Captura o erro se o arquivo CSV não for encontrado.
    *   `try...except requests.exceptions.RequestException`: Captura erros de rede ou de requisição (ex: API inacessível).
    *   Verifica `response.status_code`: Permite identificar se a requisição foi bem-sucedida (códigos 2xx) ou se houve um erro (códigos 4xx ou 5xx).
*   **`batch_size`**: Permite agrupar várias linhas do CSV em uma única requisição HTTP, se a API de destino suportar essa forma de entrada (geralmente uma lista de objetos JSON).
*   **`delay_between_requests`**: Ajuda a evitar exceder os limites de taxa de uma API ao introduzir um pequeno atraso entre cada requisição (ou batch).
*   **Resumo**: Ao final, o script imprime um resumo das operações realizadas.

Este script é uma base sólida para integrar dados CSV com APIs externas. Lembre-se de sempre adaptar a estrutura do `payload` e os cabeçalhos às especificações da API que você está utilizando.

Time taken: 26.79565143585205 seconds
Tokens used: 4603