O aviso **UnhandledPromiseRejectionWarning** acontece porque a Promise retornada pela função assíncrona `fetchData` pode rejeitar (por exemplo, se a requisição falhar), mas você não está tratando esse erro com um bloco `try/catch` ou um método `.catch()`.

No seu código, a função `fetchData()` pode gerar um erro que não está sendo capturado, gerando esse aviso.

---

### Como corrigir

1. **Usando try/catch dentro da função `fetchData`:**
```js
const axios = require("axios");

async function fetchData() {
  try {
    const res = await axios.get("https://api.com/dados");
    console.log(res.data);
  } catch (error) {
    console.error("Erro ao buscar dados:", error.message);
  }
}

fetchData();
```

2. **Ou tratando a Promise no momento de chamar a função:**
```js
fetchData().catch(error => {
  console.error("Erro ao buscar dados:", error.message);
});
```

---

### Explicação

- Quando uma Promise rejeita e você não trata esse erro, o Node.js emite o `UnhandledPromiseRejectionWarning`.
- Sempre trate erros em funções async (com try/catch) ou diretamente nas Promises (com `.catch()`).
- Isso evita que o processo do Node seja encerrado inesperadamente e ajuda no debug das aplicações.

---

Se quiser garantir que seu código trate erros async de forma elegante, sempre mantenha blocos `try/catch` para chamadas await, especialmente ao usar axios ou outras operações que dependem de IO e podem falhar.

Time taken: 4.62438702583313 seconds
Tokens used: 407