Este é um middleware de autenticação JWT completo para Node.js, abrangendo a geração, verificação e renovação de tokens. Ele utiliza tokens de acesso de curta duração e tokens de atualização (refresh tokens) de longa duração para uma segurança aprimorada.

Vamos organizar o código em uma estrutura de projeto típica.

### Estrutura do Projeto

```
jwt-auth-middleware-example/
├── .env                  # Variáveis de ambiente
├── package.json
├── app.js                # Arquivo principal da aplicação Express
├── config/
│   └── index.js          # Configurações globais
├── utils/
│   └── jwtUtils.js       # Funções utilitárias para JWT
├── middleware/
│   └── authMiddleware.js # Middleware de autenticação
├── controllers/
│   └── authController.js # Lógica de autenticação (login, register, refresh, logout)
├── routes/
│   ├── authRoutes.js     # Rotas de autenticação
│   └── protectedRoutes.js# Exemplo de rotas protegidas
└── models/
    └── User.js           # Modelo de usuário (simulado para este exemplo)
```

### 1. Inicialização do Projeto

Primeiro, crie a pasta do projeto e inicialize-o:

```bash
mkdir jwt-auth-middleware-example
cd jwt-auth-middleware-example
npm init -y
```

### 2. Instalar Dependências

```bash
npm install express jsonwebtoken dotenv bcryptjs
```

### 3. Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto para armazenar as chaves secretas e outras configurações importantes.

**`.env`**
```env
PORT=3000

# Segredos JWT (GERAR CHAVES FORTES E ÚNICAS)
# Exemplo: Abra um terminal e execute `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"` para gerar uma chave.
JWT_ACCESS_SECRET=suaChaveSecretaDeAcessoForteEJNICA
JWT_REFRESH_SECRET=suaChaveSecretaDeAtualizacaoForteEJNICA

# Duração dos tokens (Exemplos: '15m', '1h', '7d')
ACCESS_TOKEN_EXPIRATION='15m'
REFRESH_TOKEN_EXPIRATION='7d'
```

### 4. `config/index.js` (Configurações)

Este arquivo carrega as variáveis de ambiente e exporta as configurações.

**`config/index.js`**
```javascript
require('dotenv').config();

module.exports = {
  port: process.env.PORT || 3000,
  jwt: {
    accessSecret: process.env.JWT_ACCESS_SECRET,
    refreshSecret: process.env.JWT_REFRESH_SECRET,
    accessTokenExpiration: process.env.ACCESS_TOKEN_EXPIRATION,
    refreshTokenExpiration: process.env.REFRESH_TOKEN_EXPIRATION,
  },
};
```

### 5. `models/User.js` (Simulação de Modelo de Usuário)

Para simplificar, usaremos um array em memória para usuários. Em uma aplicação real, você usaria um banco de dados (MongoDB, PostgreSQL, etc.) com Mongoose, Sequelize ou Prisma.

**`models/User.js`**
```javascript
const bcrypt = require('bcryptjs');

// Simulação de banco de dados em memória
const users = []; // Armazena objetos { id, username, passwordHash, refreshTokens: [] }

const User = {
  async create(username, password) {
    const id = users.length + 1;
    const passwordHash = await bcrypt.hash(password, 10);
    const newUser = { id, username, passwordHash, refreshTokens: [] };
    users.push(newUser);
    return newUser;
  },

  findByUsername(username) {
    return users.find(user => user.username === username);
  },

  findById(id) {
    return users.find(user => user.id === id);
  },

  async comparePassword(candidatePassword, passwordHash) {
    return bcrypt.compare(candidatePassword, passwordHash);
  },

  addRefreshToken(userId, token) {
    const user = this.findById(userId);
    if (user) {
      user.refreshTokens.push(token);
      return true;
    }
    return false;
  },

  removeRefreshToken(userId, token) {
    const user = this.findById(userId);
    if (user) {
      user.refreshTokens = user.refreshTokens.filter(t => t !== token);
      return true;
    }
    return false;
  },

  hasRefreshToken(userId, token) {
    const user = this.findById(userId);
    return user ? user.refreshTokens.includes(token) : false;
  }
};

module.exports = User;
```

### 6. `utils/jwtUtils.js` (Utilitários JWT)

Funções para gerar e verificar tokens.

**`utils/jwtUtils.js`**
```javascript
const jwt = require('jsonwebtoken');
const config = require('../config');

const generateAccessToken = (userPayload) => {
  return jwt.sign(userPayload, config.jwt.accessSecret, {
    expiresIn: config.jwt.accessTokenExpiration,
  });
};

const generateRefreshToken = (userPayload) => {
  return jwt.sign(userPayload, config.jwt.refreshSecret, {
    expiresIn: config.jwt.refreshTokenExpiration,
  });
};

const verifyAccessToken = (token) => {
  try {
    return jwt.verify(token, config.jwt.accessSecret);
  } catch (error) {
    throw new Error('Access token inválido ou expirado.');
  }
};

const verifyRefreshToken = (token) => {
  try {
    return jwt.verify(token, config.jwt.refreshSecret);
  } catch (error) {
    throw new Error('Refresh token inválido ou expirado.');
  }
};

module.exports = {
  generateAccessToken,
  generateRefreshToken,
  verifyAccessToken,
  verifyRefreshToken,
};
```

### 7. `middleware/authMiddleware.js` (Middleware de Autenticação)

Este é o middleware principal para proteger as rotas.

**`middleware/authMiddleware.js`**
```javascript
const { verifyAccessToken } = require('../utils/jwtUtils');

const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Espera "Bearer TOKEN"

  if (!token) {
    return res.status(401).json({ message: 'Token de acesso não fornecido.' });
  }

  try {
    const user = verifyAccessToken(token);
    req.user = user; // Anexa o payload do usuário ao objeto de requisição
    next();
  } catch (error) {
    if (error.message.includes('expirado')) {
      return res.status(401).json({ message: 'Token de acesso expirado.', code: 'TOKEN_EXPIRED' });
    }
    return res.status(403).json({ message: 'Token de acesso inválido.', error: error.message });
  }
};

module.exports = {
  authenticateToken,
};
```

### 8. `controllers/authController.js` (Controlador de Autenticação)

Aqui está a lógica para registrar, logar, renovar tokens e fazer logout.

**`controllers/authController.js`**
```javascript
const User = require('../models/User');
const { generateAccessToken, generateRefreshToken, verifyRefreshToken } = require('../utils/jwtUtils');

const register = async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ message: 'Nome de usuário e senha são obrigatórios.' });
  }

  try {
    const existingUser = User.findByUsername(username);
    if (existingUser) {
      return res.status(409).json({ message: 'Nome de usuário já existe.' });
    }

    const newUser = await User.create(username, password);
    res.status(201).json({ message: 'Usuário registrado com sucesso!', userId: newUser.id });
  } catch (error) {
    console.error('Erro ao registrar usuário:', error);
    res.status(500).json({ message: 'Erro interno do servidor.' });
  }
};

const login = async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ message: 'Nome de usuário e senha são obrigatórios.' });
  }

  try {
    const user = User.findByUsername(username);
    if (!user) {
      return res.status(401).json({ message: 'Credenciais inválidas.' });
    }

    const isMatch = await User.comparePassword(password, user.passwordHash);
    if (!isMatch) {
      return res.status(401).json({ message: 'Credenciais inválidas.' });
    }

    const userPayload = { id: user.id, username: user.username };
    const accessToken = generateAccessToken(userPayload);
    const refreshToken = generateRefreshToken(userPayload);

    // Armazenar o refresh token no "banco de dados" para este usuário
    // Isso permite revogação de tokens e logout seguro
    User.addRefreshToken(user.id, refreshToken);

    res.json({
      message: 'Login bem-sucedido!',
      accessToken,
      refreshToken,
    });
  } catch (error) {
    console.error('Erro ao fazer login:', error);
    res.status(500).json({ message: 'Erro interno do servidor.' });
  }
};

const refresh = async (req, res) => {
  const { refreshToken } = req.body;
  if (!refreshToken) {
    return res.status(401).json({ message: 'Refresh token não fornecido.' });
  }

  try {
    const decoded = verifyRefreshToken(refreshToken);
    const user = User.findById(decoded.id);

    if (!user || !User.hasRefreshToken(user.id, refreshToken)) {
      // Se o refresh token não está no BD ou não pertence ao usuário, ele é inválido/revogado
      return res.status(403).json({ message: 'Refresh token inválido ou revogado.' });
    }

    // Gerar um novo access token
    const userPayload = { id: user.id, username: user.username };
    const newAccessToken = generateAccessToken(userPayload);

    // Opcional: Gerar um novo refresh token e invalidar o antigo para segurança adicional (rotação de refresh tokens)
    // Para simplificar, neste exemplo, vamos manter o refresh token original válido até expirar.
    // Em um cenário de rotação, você removeria o refreshToken antigo e adicionaria o novo:
    // User.removeRefreshToken(user.id, refreshToken);
    // const newRefreshToken = generateRefreshToken(userPayload);
    // User.addRefreshToken(user.id, newRefreshToken);
    // res.json({ accessToken: newAccessToken, refreshToken: newRefreshToken });

    res.json({ accessToken: newAccessToken });
  } catch (error) {
    console.error('Erro ao renovar token:', error);
    if (error.message.includes('expirado')) {
      return res.status(403).json({ message: 'Refresh token expirado. Por favor, faça login novamente.', code: 'REFRESH_TOKEN_EXPIRED' });
    }
    res.status(403).json({ message: 'Refresh token inválido.', error: error.message });
  }
};

const logout = async (req, res) => {
  const { refreshToken } = req.body;
  if (!refreshToken) {
    return res.status(400).json({ message: 'Refresh token não fornecido.' });
  }

  try {
    const decoded = verifyRefreshToken(refreshToken);
    const user = User.findById(decoded.id);

    if (user) {
      // Remove o refresh token do "banco de dados"
      User.removeRefreshToken(user.id, refreshToken);
    }
    // Mesmo se o token não for encontrado ou usuário não existir, retornamos sucesso
    // para evitar vazamento de informações.
    res.status(200).json({ message: 'Logout realizado com sucesso.' });
  } catch (error) {
    // Se o refresh token já estiver expirado ou inválido, apenas confirmamos o logout.
    res.status(200).json({ message: 'Logout realizado com sucesso (refresh token já inválido ou expirado).' });
  }
};

module.exports = {
  register,
  login,
  refresh,
  logout,
};
```

### 9. `routes/authRoutes.js` (Rotas de Autenticação)

Define as rotas para registro, login, renovação e logout.

**`routes/authRoutes.js`**
```javascript
const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

router.post('/register', authController.register);
router.post('/login', authController.login);
router.post('/refresh', authController.refresh);
router.post('/logout', authController.logout);

module.exports = router;
```

### 10. `routes/protectedRoutes.js` (Exemplo de Rotas Protegidas)

Exemplo de como usar o middleware de autenticação.

**`routes/protectedRoutes.js`**
```javascript
const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/authMiddleware');

// Esta rota só pode ser acessada com um token de acesso válido
router.get('/data', authenticateToken, (req, res) => {
  res.json({
    message: 'Bem-vindo ao recurso protegido!',
    user: req.user, // O payload do usuário anexado pelo middleware
    data: 'Dados sensíveis aqui.',
  });
});

module.exports = router;
```

### 11. `app.js` (Arquivo Principal da Aplicação)

Configura o servidor Express e as rotas.

**`app.js`**
```javascript
const express = require('express');
const config = require('./config');
const authRoutes = require('./routes/authRoutes');
const protectedRoutes = require('./routes/protectedRoutes');

const app = express();

// Middleware para parsear JSON no corpo da requisição
app.use(express.json());

// Rotas de Autenticação
app.use('/auth', authRoutes);

// Rotas Protegidas
app.use('/protected', protectedRoutes);

// Rota de teste
app.get('/', (req, res) => {
  res.send('Servidor de autenticação JWT rodando!');
});

// Tratamento de erros (opcional, mas recomendado)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Algo deu errado!');
});

app.listen(config.port, () => {
  console.log(`Servidor rodando na porta ${config.port}`);
  console.log(`Acesse http://localhost:${config.port}`);
});
```

### Como Testar

1.  **Inicie o servidor:**
    ```bash
    node app.js
    ```
    Você verá a mensagem: `Servidor rodando na porta 3000`.

2.  **Use uma ferramenta como Postman, Insomnia ou `curl`:**

    **a. Registrar um Usuário (POST /auth/register)**
    *   **URL:** `http://localhost:3000/auth/register`
    *   **Method:** `POST`
    *   **Headers:** `Content-Type: application/json`
    *   **Body (raw JSON):**
        ```json
        {
            "username": "testuser",
            "password": "password123"
        }
        ```
    *   **Resposta esperada:** `{"message":"Usuário registrado com sucesso!","userId":1}`

    **b. Fazer Login (POST /auth/login)**
    *   **URL:** `http://localhost:3000/auth/login`
    *   **Method:** `POST`
    *   **Headers:** `Content-Type: application/json`
    *   **Body (raw JSON):**
        ```json
        {
            "username": "testuser",
            "password": "password123"
        }
        ```
    *   **Resposta esperada:**
        ```json
        {
            "message": "Login bem-sucedido!",
            "accessToken": "eyJ...", // Seu token de acesso
            "refreshToken": "eyJ..." // Seu refresh token
        }
        ```
        *Guarde o `accessToken` e o `refreshToken`.*

    **c. Acessar Rota Protegida (GET /protected/data)**
    *   **Com token inválido/ausente:**
        *   **URL:** `http://localhost:3000/protected/data`
        *   **Method:** `GET`
        *   **Sem Headers de Autorização**
        *   **Resposta esperada:** `{"message":"Token de acesso não fornecido."}` (Status 401)

    *   **Com token válido:**
        *   **URL:** `http://localhost:3000/protected/data`
        *   **Method:** `GET`
        *   **Headers:** `Authorization: Bearer <seu_accessToken_aqui>` (Substitua `<seu_accessToken_aqui>` pelo token obtido no login)
        *   **Resposta esperada:**
            ```json
            {
                "message": "Bem-vindo ao recurso protegido!",
                "user": {
                    "id": 1,
                    "username": "testuser",
                    "iat": ...,
                    "exp": ...
                },
                "data": "Dados sensíveis aqui."
            }
            ```

    **d. Renovar Token (POST /auth/refresh)**
    *   **URL:** `http://localhost:3000/auth/refresh`
    *   **Method:** `POST`
    *   **Headers:** `Content-Type: application/json`
    *   **Body (raw JSON):**
        ```json
        {
            "refreshToken": "<seu_refreshToken_aqui>"
        }
        ```
    *   **Resposta esperada:**
        ```json
        {
            "accessToken": "eyJ..." // Um novo token de acesso
        }
        ```
        *Seu token de acesso antigo pode ter expirado, mas com o refresh token, você obtém um novo.*

    **e. Fazer Logout (POST /auth/logout)**
    *   **URL:** `http://localhost:3000/auth/logout`
    *   **Method:** `POST`
    *   **Headers:** `Content-Type: application/json`
    *   **Body (raw JSON):**
        ```json
        {
            "refreshToken": "<seu_refreshToken_aqui>"
        }
        ```
    *   **Resposta esperada:** `{"message":"Logout realizado com sucesso."}`
    *   *Após o logout, o refresh token se torna inválido. Se você tentar usá-lo novamente, receberá `Refresh token inválido ou revogado.`*

Este setup fornece uma base robusta para autenticação JWT, cobrindo os principais fluxos de trabalho e incorporando boas práticas como refresh tokens e o armazenamento seguro deles no lado do servidor para revogação.

Time taken: 29.905152320861816 seconds
Tokens used: 6481