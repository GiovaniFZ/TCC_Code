Claro! Aqui está uma função em TypeScript que valida emails e números de telefone utilizando expressões regulares (regex):

```typescript
function validarEmail(email: string): boolean {
    // Regex simples e comum para validação de email
    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regexEmail.test(email);
}

function validarTelefone(telefone: string): boolean {
    // Regex para números de telefone no formato brasileiro, com DDD e 8 ou 9 dígitos
    // Exemplo de formatos válidos:
    // (11) 98765-4321
    // 11987654321
    // 11 98765-4321
    // +55 11 98765-4321
    // 98765-4321 (sem DDD, opcional)
    const regexTelefone = /^(\+55\s?)?(\(?\d{2}\)?\s?)?9?\d{4}-?\d{4}$/;
    return regexTelefone.test(telefone);
}

// Exemplo de uso
console.log(validarEmail("exemplo@test.com"));        // true
console.log(validarEmail("email_invalido@.com"));     // false

console.log(validarTelefone("(11) 98765-4321"));       // true
console.log(validarTelefone("+55 11 98765-4321"));    // true
console.log(validarTelefone("98765-4321"));           // true
console.log(validarTelefone("1234"));                 // false
```

### Explicação

- **Email**: O regex usado é simples, verifica se há algo antes do `@`, um domínio e uma extensão separados por pontos. Não é perfeito (não valida todos os casos possíveis do padrão RFC), mas cobre a maioria dos casos comuns.
- **Telefone**: O regex cobre:
  - Código do país opcional (+55)
  - Código de área opcional de 2 dígitos, com ou sem parênteses
  - Número de telefone que pode começar com 9 (telefone móvel no Brasil tem 9 dígitos começando com 9)
  - Quatro dígitos, depois um hífen opcional, e mais quatro dígitos

Se quiser que eu ajuste para outro formato de telefone ou regex mais específico, é só avisar!

Time taken: 6.672101020812988 seconds
Tokens used: 539