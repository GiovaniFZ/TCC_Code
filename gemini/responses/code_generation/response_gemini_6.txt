Com certeza! Vamos criar uma API REST em Node.js usando Express, Sequelize e MySQL para gerenciar produtos.

### Pré-requisitos:

1.  **Node.js e npm:** Certifique-se de ter o Node.js instalado (inclui o npm).
2.  **MySQL Server:** Tenha um servidor MySQL rodando. Você pode usar XAMPP, Docker, ou uma instalação nativa.
3.  **Cliente MySQL (Opcional, mas útil):** Ferramentas como MySQL Workbench, DBeaver ou DataGrip para gerenciar seu banco de dados.

### 1. Configuração do Projeto

Crie uma nova pasta para o seu projeto e inicialize-o:

```bash
mkdir product-api
cd product-api
npm init -y
```

### 2. Instalar Dependências

Instale as bibliotecas necessárias:

```bash
npm install express sequelize mysql2 dotenv
npm install --save-dev nodemon
```

*   `express`: Framework web para Node.js.
*   `sequelize`: ORM (Object-Relational Mapper) para interagir com o banco de dados.
*   `mysql2`: Driver MySQL para o Sequelize.
*   `dotenv`: Para carregar variáveis de ambiente de um arquivo `.env`.
*   `nodemon`: Para reiniciar automaticamente o servidor durante o desenvolvimento.

### 3. Estrutura de Pastas

Organize seu projeto da seguinte forma:

```
product-api/
├── .env
├── package.json
├── package-lock.json
└── src/
    ├── app.js
    ├── config/
    │   └── database.js
    ├── models/
    │   └── Product.js
    ├── controllers/
    │   └── productController.js
    └── routes/
        └── productRoutes.js
```

### 4. Configuração do Banco de Dados (`.env` e `config/database.js`)

**`.env`**
Crie um arquivo `.env` na raiz do seu projeto e adicione suas credenciais do MySQL. **Substitua pelos seus próprios dados.**

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=product_api_db
PORT=3000
```

**`src/config/database.js`**
Este arquivo conterá a configuração do Sequelize.

```javascript
require('dotenv').config();

module.exports = {
  dialect: 'mysql',
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  username: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  define: {
    timestamps: true, // Adiciona createdAt e updatedAt automaticamente
    underscored: true, // Converte nomes de colunas camelCase para snake_case
  },
  logging: false, // Desabilita o log de queries SQL no console
};
```

### 5. Modelo Sequelize (`src/models/Product.js`)

Este arquivo define a estrutura da tabela `products` no banco de dados.

```javascript
const { DataTypes } = require('sequelize');
const sequelize = require('../app'); // Importa a instância do sequelize

const Product = sequelize.define('Product', {
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true, // Nome do produto deve ser único
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: true,
  },
  price: {
    type: DataTypes.DECIMAL(10, 2), // Preço com 10 dígitos totais e 2 casas decimais
    allowNull: false,
    defaultValue: 0.00,
  },
  stock: {
    type: DataTypes.INTEGER,
    allowNull: false,
    defaultValue: 0,
  },
});

module.exports = Product;
```
**Pequena correção**: A linha `const sequelize = require('../app');` no modelo é um anti-padrão comum. O ideal é que o `sequelize` seja inicializado e exportado de um arquivo de configuração/conexão de DB e depois importado em todos os modelos. Vou ajustar isso no `app.js` e na inicialização.

**Correção para `src/models/Product.js`:**
Precisamos que o `sequelize` seja passado para o modelo, ou importado de um arquivo que o inicializa. Para simplificar, vou inicializar o Sequelize no `app.js` e passá-lo para os modelos através de uma função de inicialização.

**Vamos criar um arquivo para a instância do Sequelize (`src/database/index.js`):**

```javascript
// src/database/index.js
const { Sequelize } = require('sequelize');
const dbConfig = require('../config/database');

const sequelize = new Sequelize(dbConfig);

// Testar a conexão
async function testConnection() {
  try {
    await sequelize.authenticate();
    console.log('Conexão com o banco de dados estabelecida com sucesso.');
  } catch (error) {
    console.error('Não foi possível conectar ao banco de dados:', error);
    process.exit(1); // Sai do processo se não conseguir conectar
  }
}

// Sincronizar modelos com o banco de dados
async function syncModels() {
  try {
    // `force: false` para não recriar tabelas existentes (mantém dados)
    // `alter: true` tenta fazer alterações na tabela para corresponder ao modelo
    await sequelize.sync({ alter: true });
    console.log('Modelos sincronizados com o banco de dados.');
  } catch (error) {
    console.error('Erro ao sincronizar modelos:', error);
    process.exit(1);
  }
}

module.exports = {
  sequelize,
  testConnection,
  syncModels,
};

```

**Agora, o modelo `src/models/Product.js` ficará assim:**

```javascript
// src/models/Product.js
const { DataTypes, Model } = require('sequelize');

class Product extends Model {
  static init(sequelize) {
    super.init({
      id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true,
      },
      name: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
      },
      description: {
        type: DataTypes.TEXT,
        allowNull: true,
      },
      price: {
        type: DataTypes.DECIMAL(10, 2),
        allowNull: false,
        defaultValue: 0.00,
      },
      stock: {
        type: DataTypes.INTEGER,
        allowNull: false,
        defaultValue: 0,
      },
    }, {
      sequelize,
      tableName: 'products', // Define o nome da tabela no banco de dados
    });
  }
}

module.exports = Product;
```

### 6. Controller (`src/controllers/productController.js`)

O controller contém a lógica de negócios para manipular os produtos.

```javascript
const Product = require('../models/Product'); // Importa o modelo Product

module.exports = {
  // Criar um novo produto
  async create(req, res) {
    try {
      const { name, description, price, stock } = req.body;

      if (!name || !price) {
        return res.status(400).json({ error: 'Nome e preço são obrigatórios.' });
      }

      const product = await Product.create({ name, description, price, stock });

      return res.status(201).json(product);
    } catch (error) {
      if (error.name === 'SequelizeUniqueConstraintError') {
        return res.status(409).json({ error: 'Já existe um produto com este nome.' });
      }
      console.error(error);
      return res.status(500).json({ error: 'Erro interno do servidor ao criar produto.' });
    }
  },

  // Listar todos os produtos
  async index(req, res) {
    try {
      const products = await Product.findAll();

      return res.status(200).json(products);
    } catch (error) {
      console.error(error);
      return res.status(500).json({ error: 'Erro interno do servidor ao listar produtos.' });
    }
  },

  // Obter um produto por ID
  async show(req, res) {
    try {
      const { id } = req.params;

      const product = await Product.findByPk(id);

      if (!product) {
        return res.status(404).json({ error: 'Produto não encontrado.' });
      }

      return res.status(200).json(product);
    } catch (error) {
      console.error(error);
      return res.status(500).json({ error: 'Erro interno do servidor ao buscar produto.' });
    }
  },

  // Atualizar um produto
  async update(req, res) {
    try {
      const { id } = req.params;
      const { name, description, price, stock } = req.body;

      const [updatedRows] = await Product.update(
        { name, description, price, stock },
        {
          where: { id },
        }
      );

      if (updatedRows === 0) {
        return res.status(404).json({ error: 'Produto não encontrado ou nenhum dado para atualizar.' });
      }

      const updatedProduct = await Product.findByPk(id); // Opcional: retorna o produto atualizado
      return res.status(200).json(updatedProduct);
    } catch (error) {
      if (error.name === 'SequelizeUniqueConstraintError') {
        return res.status(409).json({ error: 'Já existe um produto com este nome.' });
      }
      console.error(error);
      return res.status(500).json({ error: 'Erro interno do servidor ao atualizar produto.' });
    }
  },

  // Deletar um produto
  async delete(req, res) {
    try {
      const { id } = req.params;

      const deletedRows = await Product.destroy({
        where: { id },
      });

      if (deletedRows === 0) {
        return res.status(404).json({ error: 'Produto não encontrado.' });
      }

      return res.status(204).send(); // 204 No Content para deleção bem-sucedida
    } catch (error) {
      console.error(error);
      return res.status(500).json({ error: 'Erro interno do servidor ao deletar produto.' });
    }
  },
};
```

### 7. Rotas (`src/routes/productRoutes.js`)

Define os endpoints da API e os associa aos métodos do controller.

```javascript
const { Router } = require('express');
const productController = require('../controllers/productController');

const router = Router();

// Rota para cadastrar um novo produto
router.post('/', productController.create);

// Rota para listar todos os produtos
router.get('/', productController.index);

// Rota para obter um produto por ID
router.get('/:id', productController.show);

// Rota para atualizar um produto por ID
router.put('/:id', productController.update);

// Rota para deletar um produto por ID
router.delete('/:id', productController.delete);

module.exports = router;
```

### 8. Aplicação Principal (`src/app.js`)

Aqui montamos tudo: inicializamos o Express, conectamos ao banco de dados e definimos as rotas.

```javascript
// src/app.js
require('dotenv').config(); // Carrega as variáveis de ambiente do .env
const express = require('express');
const { sequelize, testConnection, syncModels } = require('./database'); // Importa a instância e funções do sequelize
const Product = require('./models/Product'); // Importa o modelo Product
const productRoutes = require('./routes/productRoutes');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware para parsing de JSON
app.use(express.json());

// Rotas da API
app.use('/products', productRoutes);

// Rota de teste
app.get('/', (req, res) => {
  res.send('API de Produtos está funcionando!');
});

// Inicializa o Sequelize com todos os modelos
async function initializeDatabase() {
  Product.init(sequelize); // Inicializa o modelo Product com a instância do Sequelize
  // Se houver outros modelos, inicialize-os aqui também:
  // AnotherModel.init(sequelize);

  await testConnection(); // Testa a conexão
  await syncModels();     // Sincroniza os modelos (cria/altera tabelas)
}

// Inicia o servidor após conectar e sincronizar o banco de dados
initializeDatabase().then(() => {
  app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
    console.log(`Acesse: http://localhost:${PORT}`);
  });
}).catch(error => {
  console.error('Falha ao iniciar a aplicação:', error);
  process.exit(1);
});
```

### 9. Script de Inicialização (`package.json`)

Adicione scripts ao seu `package.json` para facilitar a execução:

```json
{
  "name": "product-api",
  "version": "1.0.0",
  "description": "API REST para gerenciamento de produtos com Node.js, Express, Sequelize e MySQL.",
  "main": "src/app.js",
  "scripts": {
    "start": "node src/app.js",
    "dev": "nodemon src/app.js"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "dotenv": "^16.4.5",
    "express": "^4.19.2",
    "mysql2": "^3.9.7",
    "sequelize": "^6.37.3"
  },
  "devDependencies": {
    "nodemon": "^3.1.0"
  }
}
```

### 10. Executar a Aplicação

1.  **Crie o Banco de Dados:** Antes de rodar, certifique-se de que o banco de dados `product_api_db` (ou o nome que você definiu em `.env`) exista no seu MySQL. Você pode criá-lo com um cliente MySQL ou executando `CREATE DATABASE product_api_db;` no console MySQL.
2.  **Inicie o Servidor:**
    ```bash
    npm run dev
    ```
    Você verá mensagens indicando a conexão e sincronização do banco de dados, e que o servidor está rodando.

### Testando a API (usando Postman, Insomnia ou `curl`)

#### 1. Cadastrar um Produto (POST)

*   **URL:** `http://localhost:3000/products`
*   **Método:** `POST`
*   **Headers:** `Content-Type: application/json`
*   **Body (raw JSON):**
    ```json
    {
        "name": "Smartphone XYZ",
        "description": "Um smartphone de última geração com câmera incrível.",
        "price": 999.99,
        "stock": 100
    }
    ```
*   **Resposta esperada (201 Created):**
    ```json
    {
        "id": 1,
        "name": "Smartphone XYZ",
        "description": "Um smartphone de última geração com câmera incrível.",
        "price": "999.99",
        "stock": 100,
        "updatedAt": "2023-10-27T10:00:00.000Z",
        "createdAt": "2023-10-27T10:00:00.000Z"
    }
    ```

#### 2. Listar Todos os Produtos (GET)

*   **URL:** `http://localhost:3000/products`
*   **Método:** `GET`
*   **Resposta esperada (200 OK):**
    ```json
    [
        {
            "id": 1,
            "name": "Smartphone XYZ",
            "description": "Um smartphone de última geração com câmera incrível.",
            "price": "999.99",
            "stock": 100,
            "createdAt": "2023-10-27T10:00:00.000Z",
            "updatedAt": "2023-10-27T10:00:00.000Z"
        }
    ]
    ```

#### 3. Obter um Produto por ID (GET)

*   **URL:** `http://localhost:3000/products/1` (substitua `1` pelo ID do produto)
*   **Método:** `GET`
*   **Resposta esperada (200 OK):** (o mesmo que o item anterior, mas apenas um produto)

#### 4. Atualizar um Produto (PUT)

*   **URL:** `http://localhost:3000/products/1` (substitua `1` pelo ID do produto)
*   **Método:** `PUT`
*   **Headers:** `Content-Type: application/json`
*   **Body (raw JSON):**
    ```json
    {
        "description": "O smartphone mais potente do mercado, agora com desconto!",
        "price": 899.99,
        "stock": 95
    }
    ```
*   **Resposta esperada (200 OK):** (o produto atualizado)

#### 5. Deletar um Produto (DELETE)

*   **URL:** `http://localhost:3000/products/1` (substitua `1` pelo ID do produto)
*   **Método:** `DELETE`
*   **Resposta esperada (204 No Content):** Nenhuma resposta no corpo.

Esta API REST agora permite que você execute as operações básicas de CRUD (com exceção de "Read One" que chamei de `show`) para produtos usando Node.js, Express, Sequelize e MySQL!

Time taken: 29.495112657546997 seconds
Tokens used: 6290