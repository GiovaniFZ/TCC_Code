O aviso **`UnhandledPromiseRejectionWarning`** ocorre porque a promessa retornada por `axios.get` está sendo rejeitada (provavelmente pela URL inválida), e essa rejeição não está sendo tratada. Ou seja, o erro gerado pela requisição não está sendo capturado, o que resulta nesse aviso.

Para corrigir, você deve tratar o erro usando `try/catch` dentro da função async **ou** usar `.catch()` na promessa.

### Como corrigir:

#### Opção 1: Usar try/catch dentro da função async

```js
const axios = require("axios");

async function fetchData() {
  try {
    const res = await axios.get("https://api.invalida.com/dados");
    console.log(res.data);
  } catch (error) {
    console.error("Erro ao buscar dados:", error.message);
  }
}

fetchData();
```

#### Opção 2: Usar `.catch()` no retorno da promessa

```js
const axios = require("axios");

async function fetchData() {
  const res = await axios.get("https://api.invalida.com/dados");
  console.log(res.data);
}

fetchData().catch(error => {
  console.error("Erro ao buscar dados:", error.message);
});
```

---

### Explicação

- Quando você usa `await`, se a promessa for rejeitada (ex: erro 404, erro de rede), essa rejeição se transforma numa exceção, que precisa ser capturada (com `try/catch`).
- Se não capturar, o Node.js avisa que há uma promessa rejeitada não tratada, o que pode causar comportamentos inesperados e deve ser evitado.

---

### Dica extra

Além disso, verifique se a URL está correta, porque "https://api.invalida.com/dados" provavelmente é inválida e causará o erro.

---

Se precisar, posso ajudar a criar um exemplo completo com tratamento de erro!

Time taken: 7.659911632537842 seconds
Tokens used: 480