Claro! Abaixo está um exemplo de como criar uma API REST em Node.js com Express que permite cadastrar, listar e deletar produtos, utilizando Sequelize para conectar com um banco de dados MySQL.

---

## Passos:

1. **Configurar o projeto**
2. **Instalar dependências**
3. **Configurar Sequelize e MySQL**
4. **Criar modelo Produto**
5. **Criar rotas para cadastrar, listar e deletar produtos**
6. **Rodar o servidor**

---

### 1. Inicialize o projeto Node.js

No terminal, crie uma pasta e inicialize o projeto:

```bash
mkdir produtos-api
cd produtos-api
npm init -y
```

### 2. Instale as dependências necessárias

```bash
npm install express sequelize mysql2 body-parser
```

- `express`: framework web.
- `sequelize`: ORM para banco MySQL.
- `mysql2`: driver MySQL para Sequelize.
- `body-parser`: para interpretar o corpo das requisições JSON (no Express 4.16+ não precisa instalar, pois já tem o express.json()).

---

### 3. Código completo da API

**index.js**

```javascript
const express = require('express');
const { Sequelize, DataTypes } = require('sequelize');

const app = express();
const port = 3000;

// Middleware para parsear JSON
app.use(express.json());

// Configuração do Sequelize
const sequelize = new Sequelize('nome_do_banco', 'usuario', 'senha', {
  host: 'localhost',
  dialect: 'mysql',
});

// Testa conexão
sequelize.authenticate()
  .then(() => console.log('Conectado ao MySQL com sucesso!'))
  .catch(err => console.error('Erro ao conectar ao MySQL:', err));

// Define o modelo Produto
const Produto = sequelize.define('Produto', {
  nome: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  preco: {
    type: DataTypes.FLOAT,
    allowNull: false,
  },
}, {
  tableName: 'produtos', // Nome da tabela no MySQL
  timestamps: false,
});

// Sincroniza modelo com banco (cria tabela se não existir)
sequelize.sync()
  .then(() => console.log('Tabela Produtos sincronizada.'))
  .catch(err => console.log('Erro ao sincronizar tabela:', err));

// Rotas

// Cadastrar produto (POST /produtos)
app.post('/produtos', async (req, res) => {
  try {
    const { nome, preco } = req.body;
    if (!nome || preco === undefined) {
      return res.status(400).json({ error: 'Nome e preço são obrigatórios' });
    }

    const novoProduto = await Produto.create({ nome, preco });
    res.status(201).json(novoProduto);
  } catch (err) {
    res.status(500).json({ error: 'Erro ao cadastrar produto' });
  }
});

// Listar produtos (GET /produtos)
app.get('/produtos', async (req, res) => {
  try {
    const produtos = await Produto.findAll();
    res.json(produtos);
  } catch (err) {
    res.status(500).json({ error: 'Erro ao buscar produtos' });
  }
});

// Deletar produto (DELETE /produtos/:id)
app.delete('/produtos/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const produto = await Produto.findByPk(id);
    if (!produto) {
      return res.status(404).json({ error: 'Produto não encontrado' });
    }

    await produto.destroy();
    res.json({ message: 'Produto deletado com sucesso' });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao deletar produto' });
  }
});

// Iniciar servidor
app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
```

---

### 4. Configurar banco de dados MySQL

Certifique-se de que você tem um banco de dados MySQL criado. Exemplo para criar no MySQL:

```sql
CREATE DATABASE nome_do_banco;
```

Substitua na linha da configuração do Sequelize com seu banco, usuário e senha:

```js
const sequelize = new Sequelize('nome_do_banco', 'usuario', 'senha', {
  host: 'localhost',
  dialect: 'mysql',
});
```

---

### 5. Testar API

Inicialize o servidor:

```bash
node index.js
```

#### Exemplos de requisições:

- **Cadastrar produto**

```bash
curl -X POST http://localhost:3000/produtos -H "Content-Type: application/json" -d '{"nome":"Caneta","preco":3.5}'
```

- **Listar produtos**

```bash
curl http://localhost:3000/produtos
```

- **Deletar produto**

```bash
curl -X DELETE http://localhost:3000/produtos/1
```

---

Se precisar de algo mais avançado (com validações, autenticação, etc), posso ajudar também!

Time taken: 14.99337387084961 seconds
Tokens used: 1130