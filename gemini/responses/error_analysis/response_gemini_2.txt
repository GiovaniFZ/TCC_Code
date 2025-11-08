O erro "`Cannot read property 'map' of undefined`" é muito comum em React (e JavaScript em geral) e significa que você está tentando chamar o método `.map()` em uma variável que, naquele momento, possui o valor `undefined`.

No seu caso, a variável `products` está `undefined` quando o seu componente `ProductList` tenta renderizar. Isso geralmente acontece por um dos seguintes motivos:

1.  **O prop `products` não foi passado** para o componente `ProductList` a partir do componente pai.
2.  **Os dados ainda estão sendo carregados (assincronamente)**: A maioria das vezes, você busca dados de uma API. Enquanto os dados estão sendo buscados, `products` pode ser `undefined` ou `null` no primeiro render.
3.  **A API retornou `undefined` ou `null`** para a lista de produtos, em vez de um array vazio ou um array de produtos.

### Como resolver?

Você precisa garantir que `products` seja sempre um array antes de tentar chamar `.map()` nele. Existem algumas abordagens para isso:

#### 1. Verificação Condicional (Mais Comum e Recomendado)

Verifique se `products` existe e se é um array antes de tentar mapeá-lo. Você pode exibir uma mensagem de carregamento, uma mensagem de "nenhum produto" ou simplesmente nada, dependendo do estado.

```jsx
export default function ProductList({ products }) {
  // Opção A: Retornar algo diferente se products for undefined/null ou vazio
  if (!products) {
    // Caso 1: products é undefined (ex: dados ainda não carregados)
    return <p>Carregando produtos...</p>;
  }

  if (products.length === 0) {
    // Caso 2: products é um array vazio (ex: nenhum produto encontrado)
    return <p>Nenhum produto disponível.</p>;
  }

  // Caso 3: products é um array com itens, pode mapear
  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}
```

**Ou, de forma mais compacta com operadores lógicos (&&) e ternários (?:) para casos simples:**

```jsx
export default function ProductList({ products }) {
  return (
    <ul>
      {/* Verifica se 'products' existe (não é null/undefined) E se tem itens */}
      {products && products.length > 0 ? (
        products.map((p) => (
          <li key={p.id}>{p.name}</li>
        ))
      ) : (
        // Renderiza uma mensagem alternativa se products for null/undefined ou vazio
        <p>Nenhum produto disponível.</p>
      )}
    </ul>
  );
}
```
**Observação**: Se você quiser renderizar *nada* se `products` for vazio ou `undefined`, pode simplificar ainda mais:
```jsx
export default function ProductList({ products }) {
  return (
    <ul>
      {/* products && ... : Só executa o map se products não for null ou undefined. */}
      {/* Se products for um array vazio, map não renderizará nada, resultando em <ul></ul> */}
      {products && products.map((p) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}
```
Essa última opção renderiza uma lista `<ul>` vazia se `products` for um array vazio, e nada dentro da `<ul>` se `products` for `null` ou `undefined`. Geralmente, é melhor dar um feedback ao usuário.

#### 2. Usar um Valor Padrão para o Prop

Você pode definir um valor padrão para o prop `products` usando a desestruturação de props. Assim, se `products` não for passado (ou for `undefined`), ele automaticamente receberá um array vazio `[]`.

```jsx
export default function ProductList({ products = [] }) { // products será um array vazio se não for passado
  // Agora você tem a garantia de que products sempre será um array.
  // Você ainda pode querer verificar se ele está vazio para exibir uma mensagem.
  if (products.length === 0) {
    return <p>Nenhum produto disponível.</p>;
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
**Vantagem:** Garante que `products` é sempre um array, evitando o erro de `undefined`.
**Desvantagem:** Não distingue entre "carregando" e "nenhum produto", a menos que você adicione um `isLoading` prop separado.

### Exemplo de Uso (Componente Pai)

Para ilustrar o cenário de carregamento de dados:

```jsx
import React, { useState, useEffect } from 'react';
import ProductList from './ProductList'; // Assumindo que ProductList está em ProductList.js

function App() {
  const [products, setProducts] = useState(undefined); // Inicialmente undefined
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        // Simula uma chamada de API
        const response = await new Promise(resolve => setTimeout(() => {
          // Exemplo 1: Dados carregados com sucesso
          resolve([
            { id: 1, name: 'Produto A' },
            { id: 2, name: 'Produto B' },
            { id: 3, name: 'Produto C' },
          ]);
          // Exemplo 2: Nenhum produto
          // resolve([]);
          // Exemplo 3: Simular erro (descomente para testar)
          // throw new Error('Falha ao buscar produtos');
        }, 2000)); // 2 segundos de atraso

        setProducts(response);
      } catch (err) {
        setError(err.message);
        setProducts([]); // Define como array vazio em caso de erro para não quebrar
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) {
    return <p>Carregando dados da API...</p>;
  }

  if (error) {
    return <p>Erro: {error}</p>;
  }

  return (
    <div>
      <h1>Meus Produtos</h1>
      {/* Passa o prop products. Ele pode ser undefined, [], ou [p1, p2...] */}
      <ProductList products={products} />
    </div>
  );
}

export default App;
```

Neste exemplo, o componente `App` gerencia o estado de carregamento e o erro, e só renderiza `ProductList` quando os dados estão prontos. O `ProductList` em si ainda precisa lidar com `products` sendo um array vazio, como mostrado nas soluções acima.

A melhor abordagem é geralmente uma combinação:
1.  **No componente pai:** Lide com os estados de `loading` e `error`.
2.  **No componente filho (`ProductList`):** Use a **verificação condicional** (`if (!products) { return <p>Carregando...</p>; } if (products.length === 0) { return <p>Nenhum produto.</p>; }`) para ser robusto e independente do estado exato do `products` recebido.

Escolha a solução que melhor se adapta à lógica e feedback visual que você deseja dar ao usuário em cada um dos estados possíveis (`carregando`, `sem produtos`, `com produtos`).

Time taken: 17.14059829711914 seconds
Tokens used: 3622