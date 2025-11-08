Claro! Vou criar um exemplo completo de um middleware de autenticação JWT em Node.js utilizando o Express. O exemplo incluirá:

- Geração do token JWT (login)
- Middleware para verificar o token em rotas protegidas
- Renovação do token (refresh)

Usaremos o pacote `jsonwebtoken` para manipulação dos tokens.

---

### Passo 1: Instalar as dependências

```bash
npm init -y
npm install express jsonwebtoken bcryptjs body-parser
```

---

### Passo 2: Código completo exemplo

```js
const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

// Segredo da aplicação
const JWT_SECRET = 'seu_segredo_super_seguro';
const JWT_EXPIRES_IN = '15m'; // tempo de expiração do access token
const JWT_REFRESH_EXPIRES_IN = '7d'; // tempo de expiração do refresh token

// Simulando um banco de dados (em produção use banco real)
const users = [
  {
    id: '1',
    username: 'user1',
    passwordHash: bcrypt.hashSync('123456', 8),
  },
];

// Armazenar refresh tokens válidos (em um banco real use base de dados ou cache)
let refreshTokens = [];

// Função para gerar access token
function generateAccessToken(user) {
  return jwt.sign(
    { id: user.id, username: user.username },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRES_IN }
  );
}

// Função para gerar refresh token
function generateRefreshToken(user) {
  const refreshToken = jwt.sign(
    { id: user.id, username: user.username },
    JWT_SECRET,
    { expiresIn: JWT_REFRESH_EXPIRES_IN }
  );
  refreshTokens.push(refreshToken); // armazenar refresh token
  return refreshToken;
}

// Middleware para proteger rotas
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

  if (!token) return res.status(401).json({ message: 'Token não fornecido' });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ message: 'Token inválido ou expirado' });
    req.user = user;
    next();
  });
}

// Rota para login (gera tokens)
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  const user = users.find(u => u.username === username);
  if (!user) return res.status(400).json({ message: 'Usuário ou senha inválidos' });

  const isPasswordValid = bcrypt.compareSync(password, user.passwordHash);
  if (!isPasswordValid) return res.status(400).json({ message: 'Usuário ou senha inválidos' });

  const accessToken = generateAccessToken(user);
  const refreshToken = generateRefreshToken(user);

  res.json({
    accessToken,
    refreshToken,
  });
});

// Rota para renovar o token (refresh)
app.post('/token', (req, res) => {
  const { token } = req.body;
  if (!token) return res.status(401).json({ message: 'Refresh token não fornecido' });
  if (!refreshTokens.includes(token)) return res.status(403).json({ message: 'Refresh token inválido' });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ message: 'Refresh token expirado ou inválido' });

    const refreshedUser = { id: user.id, username: user.username };
    // Gerar novo access token
    const accessToken = generateAccessToken(refreshedUser);
    res.json({ accessToken });
  });
});

// Rota para logout (remoção do refresh token)
app.post('/logout', (req, res) => {
  const { token } = req.body;
  refreshTokens = refreshTokens.filter(t => t !== token);
  res.json({ message: 'Logout realizado com sucesso' });
});

// Rota protegida de exemplo
app.get('/protected', authenticateToken, (req, res) => {
  res.json({ message: `Olá ${req.user.username}, você acessou uma rota protegida!` });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
```

---

### Como funciona?

- **/login**: Recebe username e senha, valida e retorna o access token (válido por 15 minutos) e o refresh token (válido por 7 dias).
- **/token**: Recebe o refresh token, verifica se está armazenado e válido e retorna um novo access token.
- **/logout**: Remove o refresh token, invalidando-o para futuras renovações.
- **Middleware authenticateToken**: Verifica o access token e permite acesso a rotas protegidas.
- **/protected**: Exemplo de rota que só pode ser acessada com token válido.

---

### Testando com Curl (exemplo)

// Login
```bash
curl -X POST http://localhost:3000/login -H "Content-Type: application/json" -d "{\"username\":\"user1\",\"password\":\"123456\"}"
```

// Usando o token para acessar rota protegida (supondo o token recebido é ABC)
```bash
curl http://localhost:3000/protected -H "Authorization: Bearer ABC"
```

// Renovando token
```bash
curl -X POST http://localhost:3000/token -H "Content-Type: application/json" -d "{\"token\":\"<refresh_token>\"}"
```

---

Se precisar, posso ajudar a adaptar para seu projeto real ou com banco de dados.

Time taken: 16.545830965042114 seconds
Tokens used: 1296