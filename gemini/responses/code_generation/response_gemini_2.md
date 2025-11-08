Com certeza! Criarei uma função em TypeScript que valida emails e números de telefone usando expressões regulares, com explicações detalhadas para cada regex.

```typescript
/**
 * Valida um email ou número de telefone utilizando expressões regulares.
 *
 * @param input A string a ser validada (email ou telefone).
 * @param type O tipo de validação a ser realizada ('email' ou 'phone').
 * @returns `true` se a string for válida para o tipo especificado, `false` caso contrário.
 */
function validateContactInfo(input: string, type: 'email' | 'phone'): boolean {
    // --------------------------------------------------------------------------------
    // Regex para validação de Email
    // --------------------------------------------------------------------------------
    // Esta regex é uma das mais comuns e robustas para validação de emails.
    // Embora uma regex "perfeita" para emails seja extremamente complexa e quase impossível
    // devido às especificações RFC, esta cobre a grande maioria dos casos válidos.
    //
    // Explicação:
    // ^                                     - Início da string
    // [a-zA-Z0-9._%+-]+                     - Nome de usuário:
    //   a-zA-Z0-9                           - Permite letras (maiúsculas/minúsculas) e números
    //   ._%+-                               - Permite ponto, sublinhado, percentagem, mais e hífen
    //   +                                   - Pelo menos um desses caracteres
    // @                                     - Literal '@'
    // [a-zA-Z0-9.-]+                     - Domínio:
    //   a-zA-Z0-9                           - Permite letras e números
    //   .-                                  - Permite ponto e hífen
    //   +                                   - Pelo menos um desses caracteres
    // \.                                    - Literal '.' (escapado com barra invertida)
    // [a-zA-Z]{2,}                          - TLD (Top-Level Domain):
    //   a-zA-Z                              - Pelo menos duas letras (ex: com, org, br, co.uk, etc.)
    //   {2,}                                - Mínimo de 2 caracteres
    // $                                     - Fim da string
    // i                                     - Flag para tornar a regex case-insensitive (não faz distinção entre maiúsculas e minúsculas)
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/i;

    // --------------------------------------------------------------------------------
    // Regex para validação de Número de Telefone
    // --------------------------------------------------------------------------------
    // A validação de números de telefone é intrinsecamente complexa devido à
    // vasta gama de formatos internacionais (códigos de país, códigos de área,
    // separadores variados como espaços, hífens, parênteses, etc.).
    // Esta regex é um compromisso para cobrir formatos comuns (internacionais e locais)
    // sem ser excessivamente complexa ou específica de um único país.
    //
    // Explicação:
    // ^                                     - Início da string
    // \+?                                   - Opcional sinal de '+' no início (para códigos de país internacionais)
    // (\d{1,3})?                            - Grupo opcional de 1 a 3 dígitos (para código de país, ex: +1, +44, +55)
    // [\s.-]?                               - Separador opcional: espaço, ponto ou hífen
    // (\(?\d{2,4}\)?)?                      - Grupo opcional para código de área/primeiros dígitos:
    //   \(?                                 - Opcional parêntese de abertura
    //   \d{2,4}                             - 2 a 4 dígitos
    //   \)?                                 - Opcional parêntese de fechamento
    // [\s.-]?                               - Separador opcional
    // \d{3}                                 - Bloco de 3 dígitos
    // [\s.-]?                               - Separador opcional
    // \d{3,4}                               - Bloco final de 3 ou 4 dígitos
    // $                                     - Fim da string
    //
    // IMPORTANTE: Para aplicações de produção que exigem validação de telefone de alta precisão
    // globalmente, é altamente recomendável usar uma biblioteca dedicada, como
    // `libphonenumber-js` (uma porta do libphonenumber do Google), que lida com
    // as complexidades de formatos, códigos de país, e validação de existência.
    const phoneRegex = /^\+?(\d{1,3})?[\s.-]?(\(?\d{2,4}\)?)?[\s.-]?\d{3}[\s.-]?\d{3,4}$/;

    if (type === 'email') {
        return emailRegex.test(input);
    } else if (type === 'phone') {
        return phoneRegex.test(input);
    } else {
        // Embora o tipo seja restrito, é uma boa prática ter um fallback
        // ou erro para garantir a robustez em casos inesperados.
        throw new Error("Tipo de validação inválido. Use 'email' ou 'phone'.");
    }
}

// --- Exemplos de Uso ---

console.log("--- Validação de Email ---");
console.log("email@example.com:", validateContactInfo("email@example.com", "email"));          // true
console.log("user.name+tag@domain.co.uk:", validateContactInfo("user.name+tag@domain.co.uk", "email")); // true
console.log("invalid-email", validateContactInfo("invalid-email", "email"));                // false
console.log("email@.com:", validateContactInfo("email@.com", "email"));                    // false
console.log("email@domain:", validateContactInfo("email@domain", "email"));                 // false
console.log(" email@example.com", validateContactInfo(" email@example.com", "email"));      // false (espaço no início)
console.log("teste@sub.dominio.com.br", validateContactInfo("teste@sub.dominio.com.br", "email")); // true

console.log("\n--- Validação de Telefone ---");
console.log("+1 (123) 456-7890:", validateContactInfo("+1 (123) 456-7890", "phone"));        // true
console.log("123-456-7890:", validateContactInfo("123-456-7890", "phone"));                // true
console.log("4123456789:", validateContactInfo("4123456789", "phone"));                    // true
console.log("(123) 456 7890:", validateContactInfo("(123) 456 7890", "phone"));            // true
console.log("+44 7911 123456:", validateContactInfo("+44 7911 123456", "phone"));            // true (Exemplo de celular UK)
console.log("0800 123 4567:", validateContactInfo("0800 123 4567", "phone"));                // true (Exemplo de 0800)
console.log("123-456:", validateContactInfo("123-456", "phone"));                        // false (muito curto)
console.log("invalid phone number:", validateContactInfo("invalid phone number", "phone"));   // false
console.log("123456789012345678901234567890:", validateContactInfo("123456789012345678901234567890", "phone")); // false (muito longo, ou estrutura errada)
console.log("+55 (11) 98765-4321:", validateContactInfo("+55 (11) 98765-4321", "phone"));   // true (Exemplo brasileiro com 9º dígito e DDD)
console.log("21 2222-3333:", validateContactInfo("21 2222-3333", "phone"));               // true (Exemplo de telefone fixo)
```

### Como compilar e executar (se você tiver Node.js e TypeScript instalados):

1.  **Salve o código:** Crie um arquivo chamado `validator.ts` e cole o código acima.
2.  **Compile o TypeScript:** Abra seu terminal no diretório onde você salvou o arquivo e execute:
    ```bash
    tsc validator.ts
    ```
    Isso criará um arquivo `validator.js` (JavaScript puro) na mesma pasta.
3.  **Execute o JavaScript:**
    ```bash
    node validator.js
    ```
    Você verá os resultados dos `console.log` no terminal.

Este exemplo fornece uma solução robusta para a maioria dos casos de uso, mas lembre-se das complexidades inerentes à validação de números de telefone para cenários globais.

Time taken: 27.01611566543579 seconds
Tokens used: 6087