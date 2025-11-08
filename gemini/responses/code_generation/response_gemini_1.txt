Com certeza! Aqui está um código Python que lê um arquivo de texto, conta o número de linhas e o número total de palavras.

### Código Python

```python
import os

def contar_linhas_e_palavras(caminho_do_arquivo):
    """
    Lê um arquivo de texto, conta o número de linhas e o número de palavras.

    Args:
        caminho_do_arquivo (str): O caminho completo para o arquivo de texto.

    Returns:
        tuple: Uma tupla contendo (numero_de_linhas, numero_de_palavras).
               Retorna (0, 0) se o arquivo estiver vazio ou se houver um erro.
    """
    numero_de_linhas = 0
    numero_de_palavras = 0

    try:
        # Abrir o arquivo em modo de leitura ('r') com codificação UTF-8
        # O 'with' garante que o arquivo seja fechado automaticamente
        with open(caminho_do_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                numero_de_linhas += 1
                # Remove espaços em branco extras e quebras de linha
                # e divide a linha em uma lista de palavras
                palavras = linha.strip().split()
                numero_de_palavras += len(palavras)
        
        return numero_de_linhas, numero_de_palavras

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_do_arquivo}' não foi encontrado.")
        return 0, 0
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return 0, 0

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # 1. Nome do arquivo a ser lido
    nome_do_arquivo = "meu_texto_exemplo.txt"

    # 2. Criar um arquivo de exemplo para teste (se ele não existir)
    if not os.path.exists(nome_do_arquivo):
        print(f"Criando um arquivo de exemplo: '{nome_do_arquivo}'...")
        with open(nome_do_arquivo, 'w', encoding='utf-8') as f:
            f.write("Este é um arquivo de texto de exemplo.\n")
            f.write("Ele tem várias linhas.\n")
            f.write("Cada linha contém algumas palavras.\n")
            f.write("\n") # Linha vazia
            f.write("Fim do arquivo.")
        print("Arquivo de exemplo criado com sucesso.\n")

    # 3. Chamar a função para contar linhas e palavras
    linhas, palavras = contar_linhas_e_palavras(nome_do_arquivo)

    # 4. Exibir os resultados
    if linhas > 0 or palavras > 0: # Para evitar mostrar 0 linhas/0 palavras se houver um erro
        print(f"Resultados para o arquivo '{nome_do_arquivo}':")
        print(f"Número total de linhas: {linhas}")
        print(f"Número total de palavras: {palavras}")
```

### Como Funciona:

1.  **`contar_linhas_e_palavras(caminho_do_arquivo)` Função:**
    *   Recebe o `caminho_do_arquivo` como argumento.
    *   Inicializa `numero_de_linhas` e `numero_de_palavras` com 0.
    *   **`try...except` Bloco:** É usado para lidar com possíveis erros, como o arquivo não ser encontrado (`FileNotFoundError`) ou outros problemas de leitura.
    *   **`with open(caminho_do_arquivo, 'r', encoding='utf-8') as arquivo:`**
        *   `open()`: Abre o arquivo.
        *   `'r'`: Indica que o arquivo será aberto no modo de leitura.
        *   `encoding='utf-8'`: Define a codificação do arquivo. UTF-8 é a mais comum e recomendada.
        *   `with`: Garante que o arquivo seja automaticamente fechado, mesmo que ocorram erros.
    *   **`for linha in arquivo:`:** Itera sobre cada linha do arquivo.
        *   `numero_de_linhas += 1`: Incrementa o contador de linhas a cada iteração.
        *   `linha.strip()`: Remove quaisquer espaços em branco (incluindo quebras de linha `\n`) do início e do final da linha.
        *   `split()`: Divide a string da linha em uma lista de "palavras" usando espaços em branco como delimitadores por padrão. Se uma linha estiver vazia ou contiver apenas espaços, `split()` retornará uma lista vazia.
        *   `numero_de_palavras += len(palavras)`: Soma o número de palavras encontradas na linha atual ao contador total.
    *   Retorna a tupla `(numero_de_linhas, numero_de_palavras)`.

2.  **`if __name__ == "__main__":` Bloco:**
    *   Este bloco é executado apenas quando o script é executado diretamente (não quando importado como um módulo em outro script).
    *   **Criação de Arquivo de Exemplo:** Para facilitar o teste, o código verifica se o arquivo `meu_texto_exemplo.txt` existe. Se não existir, ele o cria com um conteúdo simples.
    *   Chama a função `contar_linhas_e_palavras()` com o nome do arquivo.
    *   Imprime os resultados formatados.

### Como Usar:

1.  **Salve o código:** Salve o código acima em um arquivo chamado, por exemplo, `contador_texto.py`.
2.  **Crie seu arquivo de texto (ou use o de exemplo):**
    *   Você pode deixar o código criar o arquivo `meu_texto_exemplo.txt` automaticamente na primeira execução.
    *   Ou, crie seu próprio arquivo de texto (e ajuste a variável `nome_do_arquivo` no código se o nome for diferente). Certifique-se de que ele esteja no mesmo diretório do script Python ou forneça o caminho completo.
3.  **Execute o script:** Abra um terminal ou prompt de comando, navegue até o diretório onde você salvou o arquivo e execute:
    ```bash
    python contador_texto.py
    ```

O script imprimirá o número de linhas e palavras encontradas no arquivo especificado.

Time taken: 12.973251819610596 seconds
Tokens used: 2728