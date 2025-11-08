Claro! Vamos entender o que são **SSR** e **SPA** no desenvolvimento web e, em seguida, eu te dou exemplos básicos de código para cada um.

---

## O que é SPA?

**SPA** (Single Page Application) é um tipo de aplicação web onde toda a navegação ocorre dentro de uma única página HTML. Em vez de recarregar a página inteira ao navegar, o conteúdo é atualizado dinamicamente via JavaScript, geralmente usando frameworks/bibliotecas como React, Vue, Angular, etc.

- **Vantagens:**
  - Experiência mais fluida e rápida para o usuário.
  - Menos carga no servidor após o carregamento inicial.
- **Desvantagens:**
  - Pode ter SEO mais desafiador (embora isso esteja melhorando).
  - SEO e performance inicial podem sofrer se não for otimizado.

---

## O que é SSR?

**SSR** (Server-Side Rendering) é uma técnica onde o HTML da página é gerado no servidor, e enviado ao cliente já pronto para ser exibido no navegador. Isso melhora performance inicial e SEO, pois os buscadores conseguem indexar conteúdo diretamente.

- Pode ser usado com JS frameworks modernos (React, Vue) usando ferramentas como Next.js, Nuxt.js.
- Também é a forma tradicional de renderização em aplicações web (exemplo: PHP, Django, Ruby on Rails).

---

## Exemplos Básicos

### 1. Exemplo simples de SPA com React

```jsx
// app.js (SPA com React)
import React, { useState } from 'react';

function App() {
  const [page, setPage] = useState('home');

  return (
    <div>
      <nav>
        <button onClick={() => setPage('home')}>Home</button>
        <button onClick={() => setPage('about')}>About</button>
      </nav>

      {page === 'home' && <h1>Bem-vindo à Home Page!</h1>}
      {page === 'about' && <h1>Sobre Nós</h1>}
    </div>
  );
}

export default App;
```

Aqui, o conteúdo muda sem recarregar a página.

---

### 2. Exemplo simples de SSR com Node.js e Express + EJS

```js
// server.js (SSR simples com Express)
const express = require('express');
const app = express();

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
  res.render('index', { pageTitle: 'Home' });
});

app.get('/about', (req, res) => {
  res.render('about', { pageTitle: 'About' });
});

app.listen(3000, () => {
  console.log('Servidor rodando na porta 3000');
});
```

E as views:

```ejs
<!-- views/index.ejs -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title><%= pageTitle %></title>
</head>
<body>
  <h1>Bem-vindo à Home Page (renderizado no servidor)!</h1>
  <a href="/about">Sobre Nós</a>
</body>
</html>
```

```ejs
<!-- views/about.ejs -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title><%= pageTitle %></title>
</head>
<body>
  <h1>Sobre Nós (renderizado no servidor)</h1>
  <a href="/">Home</a>
</body>
</html>
```

---

Se quiser, posso detalhar exemplos mais complexos em React com Next.js (SSR) ou em Vue com Nuxt.js. Quer?

Time taken: 12.002638578414917 seconds
Tokens used: 818