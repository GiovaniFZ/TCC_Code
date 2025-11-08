Esse erro geralmente acontece quando você tenta usar `require` em um ambiente que não suporta módulos CommonJS, por exemplo:

1. **Executando em um ambiente que usa módulos ES (ES Modules)**, como arquivos `.mjs` ou um projeto com `"type": "module"` no `package.json`.
2. **Tentando executar o código no navegador**, onde o `require` não existe nativamente.

### O que pode estar errado e como corrigir:

#### 1. Verifique o tipo do seu projeto no `package.json`

Se você tem no `package.json` algo assim:

```json
{
  "type": "module"
}
```

Isso indica que o Node usará módulos ES (ESM), onde **`require` não é suportado**. Nesse caso, você deve usar a sintaxe de importação ES6:

```js
import express from "express";

const app = express();

app.get("/", (req, res) => res.send("Olá!"));
app.listen(3000);
```

Salve o arquivo com `.js` normalmente e rode com o Node (v12+):

```bash
node index.js
```

#### 2. Remova `"type": "module"` ou renomeie o arquivo para `.cjs`

Se quiser continuar usando `require`:

- Remova `"type": "module"` do `package.json` (ou não crie).
- Renomeie seu arquivo para `index.cjs`.
- Rode normalmente:

```bash
node index.cjs
```

#### 3. Verifique se não está rodando o arquivo no navegador

Se está tentando executar esse código diretamente no navegador (por exemplo, usando `<script>`), o `require` não vai funcionar, pois ele é uma função do Node.js. Para usar `express`, que é um framework para Node, você deve executar no ambiente Node.js (servidor), não no cliente.

---

### Resumo

- Usando módulos ES (`"type": "module"`): use `import`.
- Usando CommonJS (padrão sem `"type": "module"`): use `require`.
- Não execute código Node que usa `require` no navegador.

Se quiser um código imediatamente compatível com Node.js padrão sem configurações, só apague `"type": "module"` e use `require`.

---

Se precisar, posso ajudar com exemplos para cada caso!

Time taken: 9.501184701919556 seconds
Tokens used: 567