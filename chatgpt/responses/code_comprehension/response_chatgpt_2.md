O algoritmo apresentado é o **Bubble Sort** (Ordenação por bolha).

### Como funciona o Bubble Sort?

1. O algoritmo percorre o array várias vezes.
2. A cada passagem, ele compara elementos adjacentes:
   - Se o elemento atual for maior que o próximo, eles são trocados de posição.
3. Assim, após cada passagem completa, o maior elemento "borbulha" para o final do array.
4. Nas próximas passagens, o algoritmo ignora os últimos elementos já ordenados, pois eles estão no lugar correto.
5. Repete esse processo até que todo o array esteja ordenado.

### Passo a passo para arr = [5, 3, 8, 4, 2]:

- Inicial: [5, 3, 8, 4, 2]

**Passagem 1 (i=0):**

- Compare 5 e 3 → 5 > 3 → troca → [3, 5, 8, 4, 2]
- Compare 5 e 8 → 5 < 8 → não troca → [3, 5, 8, 4, 2]
- Compare 8 e 4 → 8 > 4 → troca → [3, 5, 4, 8, 2]
- Compare 8 e 2 → 8 > 2 → troca → [3, 5, 4, 2, 8]

**Passagem 2 (i=1):**

- Compare 3 e 5 → 3 < 5 → não troca → [3, 5, 4, 2, 8]
- Compare 5 e 4 → 5 > 4 → troca → [3, 4, 5, 2, 8]
- Compare 5 e 2 → 5 > 2 → troca → [3, 4, 2, 5, 8]
- (Último elemento 8 está no lugar certo)

**Passagem 3 (i=2):**

- Compare 3 e 4 → 3 < 4 → não troca → [3, 4, 2, 5, 8]
- Compare 4 e 2 → 4 > 2 → troca → [3, 2, 4, 5, 8]
- (Últimos dois elementos 5,8 no lugar)

**Passagem 4 (i=3):**

- Compare 3 e 2 → 3 > 2 → troca → [2, 3, 4, 5, 8]
- (Últimos três elementos ordenados)

**Passagem 5 (i=4):**

- Apenas um elemento restante, array já ordenado.

### Saída final:
```python
[2, 3, 4, 5, 8]
```

### Resumo:

- O algoritmo é um Bubble Sort que realiza trocas sucessivas para "empurrar" os maiores elementos para o final.
- Após múltiplas passagens, o array é completamente ordenado em ordem crescente.
- Para o array dado, a saída será `[2, 3, 4, 5, 8]`.

Time taken: 10.640148639678955 seconds
Tokens used: 792