O erro **"Cannot read property ‘map’ of undefined"** ocorre porque a propriedade `products` está `undefined` no momento em que o componente `ProductList` tenta fazer o `.map()`.

Isso geralmente acontece porque:

- O prop `products` não está sendo passado para o componente.
- `products` ainda não foi inicializado (ex: dados carregando de forma assíncrona).
- Algum problema no pai que está usando esse componente.

---

### Como resolver?

1. **Defina um valor padrão para `products` para evitar que seja `undefined`:**

```js
export default function ProductList({ products = [] }) {
  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}
```

Com isso, se `products` não for passado ou for `undefined`, ele será um array vazio, e `map` funcionará sem erro.

---

2. **Verifique no componente pai se está passando o prop corretamente:**

```js
<ProductList products={products} />
```

E certifique-se que `products` está definido (ex: via state, prop, fetch) antes de renderizar.

---

3. **Se `products` vem de uma requisição assíncrona, trate o carregamento:**

```js
export default function ProductList({ products }) {
  if (!products) {
    return <div>Carregando...</div>;
  }

  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}
```

---

### Resumo rápido

- Use valor padrão: `products = []`
- Verifique no pai se está passando corretamente o prop.
- Trate estados de loading ou ausência com condicionais.

Se precisar, posso ajudar a revisar o código que consome esse componente.

Time taken: 7.460872411727905 seconds
Tokens used: 487