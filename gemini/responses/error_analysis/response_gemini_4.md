A mensagem `UnhandledPromiseRejectionWarning` no Node.js significa que uma Promise foi rejeitada (ou seja, ocorreu um erro), mas não havia nenhum manipulador de erro (`.catch()` ou `try...catch` para `async/await`) para capturar essa rejeição.

No seu caso, `axios.get()` retorna uma Promise. Se a requisição HTTP falhar (por exemplo, a URL não existe, o servidor está offline, erro de rede, ou o servidor responde com um status 4xx/5xx), essa Promise será rejeitada. Como você está usando `await`, essa rejeição se propaga como uma exceção que precisa ser capturada.

**A solução é usar um bloco `try...catch` dentro da sua função `async` para lidar com os possíveis erros.**

```javascript
const axios = require("axios");

async function fetchData() {
  try {
    // Tenta fazer a requisição HTTP
    const res = await axios.get("https://api.com/dados"); // <<<< Substitua por uma URL real para testar
    console.log("Dados recebidos:", res.data);
  } catch (error) {
    // Captura qualquer erro que ocorra durante a requisição
    console.error("Erro ao buscar dados:");

    // Detalhes do erro podem ser muito úteis para depuração
    if (axios.isAxiosError(error)) {
      // É um erro do Axios
      if (error.response) {
        // O servidor respondeu com um status diferente de 2xx
        console.error("  Status do erro:", error.response.status);
        console.error("  Dados do erro:", error.response.data);
        console.error("  Headers do erro:", error.response.headers);
      } else if (error.request) {
        // A requisição foi feita, mas nenhuma resposta foi recebida
        console.error("  Nenhuma resposta recebida:", error.request);
      } else {
        // Algo aconteceu na configuração da requisição que disparou um erro
        console.error("  Erro na requisição:", error.message);
      }
      console.error("  Configuração da requisição:", error.config);
    } else {
      // É um erro não-Axios (ex: erro de programação)
      console.error("  Erro desconhecido:", error);
    }
  }
}

fetchData();
```

**Explicação:**

1.  **`try`**: O código dentro do bloco `try` é o que você espera que seja executado com sucesso. Se tudo correr bem, `axios.get()` vai resolver, e `res.data` será logado.
2.  **`catch (error)`**: Se *qualquer* código dentro do bloco `try` lançar uma exceção (como quando `axios.get()` rejeita a Promise), a execução salta imediatamente para o bloco `catch`. A variável `error` conterá o objeto de erro.
3.  **`axios.isAxiosError(error)`**: É uma função utilitária do Axios para verificar se o erro capturado é de fato um erro gerado pelo Axios, o que permite um tratamento mais específico.
4.  **`error.response`**: Se o servidor respondeu, mas com um código de status de erro (404 Not Found, 500 Internal Server Error, etc.), os detalhes estarão em `error.response`.
5.  **`error.request`**: Se a requisição foi feita mas nenhuma resposta foi recebida (por exemplo, problema de rede, servidor não iniciou), os detalhes estarão em `error.request`.
6.  **`error.message`**: Uma mensagem de erro geral.
7.  **`error.config`**: A configuração do Axios usada para a requisição.

Ao adicionar o `try...catch`, você está garantindo que todas as rejeições de Promises (erros) sejam tratadas, eliminando o `UnhandledPromiseRejectionWarning`.

Time taken: 11.742113828659058 seconds
Tokens used: 2308