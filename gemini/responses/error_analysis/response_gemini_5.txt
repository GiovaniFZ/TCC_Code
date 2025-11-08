O erro `TypeError: Cannot destructure property 'name' of 'req.body' as it is undefined` significa que `req.body` está **indefinido** no momento em que você tenta desestruturar `name` e `price` dele.

Isso é um problema muito comum no Express e a causa quase sempre é a **falta de um middleware para fazer o parsing do corpo da requisição**. Por padrão, o Express não analisa o corpo das requisições POST, PUT, etc. Você precisa dizer a ele como fazer isso.

### A Causa: Ausência de Middleware de Body Parsing

Quando um cliente envia dados para o seu servidor Express (por exemplo, via um formulário HTML ou uma requisição JSON de uma API), esses dados chegam como um "stream". O Express, por si só, não sabe como "ler" ou "interpretar" esse stream e convertê-lo em um objeto JavaScript acessível via `req.body`.

Você precisa usar um middleware para isso. Os mais comuns são:

1.  **`express.json()`**: Para requisições que enviam dados no formato JSON (o mais comum para APIs REST).
    *   `Content-Type: application/json`
2.  **`express.urlencoded()`**: Para requisições que enviam dados no formato "URL-encoded" (o mais comum para formulários HTML tradicionais).
    *   `Content-Type: application/x-www-form-urlencoded`

### A Solução: Adicionar o Middleware

Você precisa adicionar `app.use(express.json());` (ou `app.use(express.urlencoded());` dependendo do tipo de dado que espera) **antes** de suas rotas.

```js
import express from "express";
const app = express();

// 1. Adicione este middleware para fazer o parsing de corpos de requisição JSON
//    Isso fará com que req.body seja populado com os dados JSON.
app.use(express.json());

// Se você também espera dados de formulário HTML tradicionais (URL-encoded), adicione:
// app.use(express.urlencoded({ extended: true }));
// `extended: true` permite o parsing de objetos e arrays aninhados.

app.post("/create", (req, res) => {
  // Agora req.body estará definido se a requisição tiver um corpo JSON válido
  console.log("Corpo da Requisição:", req.body); // Útil para depuração
  const { name, price } = req.body;

  // Boa prática: Valide se os dados existem antes de usá-los
  if (!name || !price) {
    return res
      .status(400)
      .json({ error: "Nome e preço são obrigatórios." });
  }

  return res.json({
    message: "Produto criado com sucesso!",
    product: { name, price },
  });
});

app.listen(3000, () => console.log("Servidor rodando na porta 3000"));
```

### Como Testar (Exemplo com `curl`):

Para testar seu servidor com a correção, você precisa enviar uma requisição que tenha o cabeçalho `Content-Type: application/json` e um corpo JSON.

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"name": "Mouse Gamer", "price": 199.99}' \
     http://localhost:3000/create
```

Se você não incluir o cabeçalho `Content-Type: application/json` ou enviar um corpo inválido, o `req.body` ainda pode ser um objeto vazio ou o parsing pode falhar de outras maneiras (mas não será `undefined` se o middleware estiver configurado corretamente para o tipo de conteúdo esperado).

Time taken: 9.23040223121643 seconds
Tokens used: 2015