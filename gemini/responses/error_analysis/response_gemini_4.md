Você está recebendo `UnhandledPromiseRejectionWarning` porque a Promise retornada por `axios.get()` está sendo rejeitada (ou seja, está falhando) e não há um bloco `catch` (ou `try...catch` em uma função `async`) para lidar com essa rejeição.

No seu caso, o URL `https://api.invalida.com/dados` é, como o nome sugere, um domínio inválido ou inexistente. Quando o Axios tenta fazer uma requisição para um domínio que não existe ou não responde, ele falha (a Promise é rejeitada), e como você não tem um `try...catch` em sua função `async fetchData()`, o Node.js emite esse aviso para indicar que uma rejeição de Promise não foi tratada.

### A Solução: Use `try...catch`

Para corrigir isso, você deve envolver a chamada `await axios.get()` em um bloco `try...catch`. Isso permitirá que você capture e lide com quaisquer erros que ocorram durante a requisição.

```javascript
const axios = require("axios");

async function fetchData() {
  try {
    const res = await axios.get("https://api.invalida.com/dados");
    console.log("Dados recebidos:", res.data);
  } catch (error) {
    // Aqui você trata o erro
    console.error("Ocorreu um erro ao buscar os dados:");

    // Axios tem um objeto de erro específico que pode ser útil
    if (axios.isAxiosError(error)) {
      if (error.response) {
        // O servidor respondeu com um status diferente de 2xx
        console.error("Status do erro:", error.response.status);
        console.error("Dados do erro:", error.response.data);
        console.error("Headers do erro:", error.response.headers);
      } else if (error.request) {
        // A requisição foi feita, mas nenhuma resposta foi recebida
        console.error("Nenhuma resposta foi recebida do servidor.");
      } else {
        // Algo aconteceu na configuração da requisição que disparou um erro
        console.error("Erro na configuração da requisição:", error.message);
      }
      console.error("Configuração da requisição:", error.config);
    } else {
      // Outro tipo de erro que não é do Axios
      console.error("Erro inesperado:", error.message);
    }
  }
}

// Chame a função para executar
fetchData();

// Exemplo com um URL válido para ver o sucesso (você pode descomentar para testar)
// async function fetchValidData() {
//   try {
//     const res = await axios.get("https://jsonplaceholder.typicode.com/todos/1");
//     console.log("\nDados válidos recebidos:", res.data);
//   } catch (error) {
//     console.error("Erro ao buscar dados válidos:", error.message);
//   }
// }
// fetchValidData();
```

### Explicação:

1.  **`try` bloco**: Contém o código que você espera que funcione, mas que pode gerar um erro (como a requisição HTTP).
2.  **`catch (error)` bloco**: Se qualquer erro (rejeição de Promise, exceção síncrona) ocorrer dentro do bloco `try`, a execução é imediatamente transferida para o bloco `catch`, e o objeto `error` é passado para ele.
3.  **`axios.isAxiosError(error)`**: É uma função utilitária do Axios para verificar se o erro é um erro específico do Axios, o que permite um tratamento de erro mais detalhado com base nas propriedades como `error.response`, `error.request`, etc.

Ao adicionar o `try...catch`, você está fornecendo um mecanismo para o Node.js lidar com a falha da Promise, eliminando assim o `UnhandledPromiseRejectionWarning`.

Time taken: 11.92755675315857 seconds
Tokens used: 2378