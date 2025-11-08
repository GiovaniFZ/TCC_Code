Claro! Aqui está um exemplo de código Python que lê um arquivo de texto e conta o número de linhas e palavras nele:

```python
def contar_linhas_e_palavras(nome_arquivo):
    num_linhas = 0
    num_palavras = 0

    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            num_linhas += 1
            palavras = linha.split()
            num_palavras += len(palavras)

    return num_linhas, num_palavras

if __name__ == "__main__":
    nome_arquivo = input("Digite o nome do arquivo de texto: ")
    linhas, palavras = contar_linhas_e_palavras(nome_arquivo)
    print(f"Número de linhas: {linhas}")
    print(f"Número de palavras: {palavras}")
```

Esse código:

- Abre o arquivo especificado em modo de leitura;
- Conta cada linha e, para cada linha, divide as palavras usando o método `split()`;
- Retorna e imprime o total de linhas e palavras do arquivo.

Se precisar de ajuda para algo mais, é só pedir!

Time taken: 4.777780532836914 seconds
Tokens used: 278