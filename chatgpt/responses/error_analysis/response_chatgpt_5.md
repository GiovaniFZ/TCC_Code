Esse erro ocorre porque `req.body` está `undefined` no momento em que você tenta fazer a desestruturação:

```js
const { name, price } = req.body;
```

No Express, para que o `req.body` seja preenchido automaticamente ao receber dados JSON na requisição, você precisa usar um middleware que faça o parser do corpo da requisição.

No seu código falta:

```js
app.use(express.json());
```

Esse middleware interpreta o corpo em JSON e popula `req.body`.

### Como corrigir

Adicione a linha abaixo antes de suas rotas:

```js
import express from "express";
const app = express();

app.use(express.json()); // <- middleware para parsear JSON

app.post("/create", (req, res) => {
  const { name, price } = req.body;
  return res.json({ name, price });
});

app.listen(3000, () => console.log("Server running on port 3000"));
```

### Por quê?

Sem ele:

- `req.body` é `undefined`
- Desestruturação falha e dá erro `Cannot destructure property 'name' of 'req.body' as it is undefined`

----

Se você receber dados em outro formato (ex: `application/x-www-form-urlencoded`), use o middleware correspondente:

```js
app.use(express.urlencoded({ extended: true }));
```

Mas no seu exemplo, provavelmente vai enviar JSON, então só o `express.json()` já resolve.

Time taken: 5.170989751815796 seconds
Tokens used: 409