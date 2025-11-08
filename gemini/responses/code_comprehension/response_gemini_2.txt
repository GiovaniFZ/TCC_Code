Esse algoritmo de ordenação é conhecido como **Bubble Sort** (Ordenação por Bolha).

---

### Como funciona o Bubble Sort:

O Bubble Sort é um dos algoritmos de ordenação mais simples, mas também um dos menos eficientes para grandes conjuntos de dados. Ele funciona da seguinte maneira:

1.  **Comparação Adjacente:** O algoritmo percorre a lista repetidamente, comparando cada elemento com o próximo elemento adjacente.
2.  **Troca (Swap):** Se um elemento for maior que o seu sucessor (no caso de ordenação crescente), eles são trocados de posição. Isso significa que o elemento "maior" "borbulha" para a direita, e o elemento "menor" "afunda" para a esquerda.
3.  **Repetição de Passos:** Esse processo é repetido para toda a lista. Após cada "passagem" completa pela lista, o maior elemento *não ordenado* estará na sua posição final correta, no final da parte não ordenada da lista.
4.  **Otimização Implícita:** A cada passagem (controlada pelo loop externo `for i in range(n)`), o maior elemento da sub-lista não ordenada "borbulha" até sua posição correta no final. Portanto, na próxima passagem, não precisamos verificar os últimos `i` elementos, pois eles já estão ordenados. Isso é o que a condição `n - i - 1` no loop interno faz: ela diminui o alcance do loop interno a cada iteração do loop externo.
5.  **Término:** O algoritmo termina quando `n-1` passagens foram realizadas, garantindo que todos os elementos estão em suas posições corretas.

**Características:**
*   **Complexidade de Tempo:** O(n^2) tanto no pior caso quanto no caso médio e melhor caso (nesta implementação sem a otimização de parada antecipada).
*   **Complexidade de Espaço:** O(1) (é um algoritmo de ordenação in-place, ou seja, não precisa de espaço adicional significativo).
*   **Estabilidade:** É um algoritmo de ordenação estável.

---

### Exemplo de execução para `arr = [5, 3, 8, 4, 2]`

Vamos traçar a execução do algoritmo com `arr = [5, 3, 8, 4, 2]`. O tamanho da array `n` é 5.

**Estado inicial:** `[5, 3, 8, 4, 2]`

---

**Passagem 1 (i = 0):** O loop interno `j` irá de `0` até `n - 0 - 1 = 4`. Ou seja, `j` assume valores `0, 1, 2, 3`.

*   **j = 0:** Compara `arr[0]` (5) e `arr[1]` (3). `5 > 3` é verdadeiro. Troca.
    `arr` se torna `[3, 5, 8, 4, 2]`
*   **j = 1:** Compara `arr[1]` (5) e `arr[2]` (8). `5 > 8` é falso. Não troca.
    `arr` continua `[3, 5, 8, 4, 2]`
*   **j = 2:** Compara `arr[2]` (8) e `arr[3]` (4). `8 > 4` é verdadeiro. Troca.
    `arr` se torna `[3, 5, 4, 8, 2]`
*   **j = 3:** Compara `arr[3]` (8) e `arr[4]` (2). `8 > 2` é verdadeiro. Troca.
    `arr` se torna `[3, 5, 4, 2, 8]`
*   **Fim da Passagem 1.** O maior elemento (8) está agora na sua posição final.

---

**Passagem 2 (i = 1):** O loop interno `j` irá de `0` até `n - 1 - 1 = 3`. Ou seja, `j` assume valores `0, 1, 2`.

*   **j = 0:** Compara `arr[0]` (3) e `arr[1]` (5). `3 > 5` é falso. Não troca.
    `arr` continua `[3, 5, 4, 2, 8]`
*   **j = 1:** Compara `arr[1]` (5) e `arr[2]` (4). `5 > 4` é verdadeiro. Troca.
    `arr` se torna `[3, 4, 5, 2, 8]`
*   **j = 2:** Compara `arr[2]` (5) e `arr[3]` (2). `5 > 2` é verdadeiro. Troca.
    `arr` se torna `[3, 4, 2, 5, 8]`
*   **Fim da Passagem 2.** O segundo maior elemento (5) está agora na sua posição final.

---

**Passagem 3 (i = 2):** O loop interno `j` irá de `0` até `n - 2 - 1 = 2`. Ou seja, `j` assume valores `0, 1`.

*   **j = 0:** Compara `arr[0]` (3) e `arr[1]` (4). `3 > 4` é falso. Não troca.
    `arr` continua `[3, 4, 2, 5, 8]`
*   **j = 1:** Compara `arr[1]` (4) e `arr[2]` (2). `4 > 2` é verdadeiro. Troca.
    `arr` se torna `[3, 2, 4, 5, 8]`
*   **Fim da Passagem 3.** O terceiro maior elemento (4) está agora na sua posição final.

---

**Passagem 4 (i = 3):** O loop interno `j` irá de `0` até `n - 3 - 1 = 1`. Ou seja, `j` assume valor `0`.

*   **j = 0:** Compara `arr[0]` (3) e `arr[1]` (2). `3 > 2` é verdadeiro. Troca.
    `arr` se torna `[2, 3, 4, 5, 8]`
*   **Fim da Passagem 4.** O quarto maior elemento (3) está agora na sua posição final.

---

**Passagem 5 (i = 4):** O loop interno `j` irá de `0` até `n - 4 - 1 = 0`. O range é `range(0, 0)`, o que significa que o loop interno **não será executado**. A array já está totalmente ordenada.

---

### Saída final:

Após todas as passagens, a array `arr` será `[2, 3, 4, 5, 8]`.

Portanto, a saída para `sort([5, 3, 8, 4, 2])` será `[2, 3, 4, 5, 8]`.

Time taken: 15.750641345977783 seconds
Tokens used: 3739