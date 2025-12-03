# Trabalho de Conclusão de Curso (TCC)

## Análise Comparativa de Desempenho de Grandes Modelos de Linguagem no Suporte ao Desenvolvimento de Software

---

## Resumo

Este trabalho apresenta uma análise comparativa do desempenho de dois Grandes Modelos de Linguagem (LLMs) - **ChatGPT (GPT-4.1-mini)** e **Gemini (Gemini 2.5 Flash)** - em tarefas fundamentais do desenvolvimento de software. A pesquisa avalia a capacidade desses modelos em três dimensões críticas: compreensão de código, geração de código e análise/correção de erros, utilizando um conjunto padronizado de 18 prompts (6 por categoria) para garantir uma comparação objetiva e reprodutível.

## Objetivos

### Objetivo Geral
Comparar sistematicamente o desempenho de diferentes LLMs em tarefas relacionadas ao desenvolvimento de software, identificando suas capacidades, limitações e áreas de aplicação mais adequadas.

### Objetivos Específicos
- Avaliar a capacidade de compreensão de código-fonte dos modelos
- Analisar a qualidade e funcionalidade do código gerado
- Verificar a eficácia na identificação e correção de erros
- Comparar métricas de desempenho (tempo de resposta e consumo de tokens)
- Identificar padrões de consistência e precisão técnica nas respostas

## Metodologia

### Modelos Avaliados
- **ChatGPT**: GPT-4.1-mini (via OpenAI API)
- **Gemini**: Gemini 2.5 Flash (via Google Generative AI API)

### Critérios de Avaliação

#### 1. Compreensão de Código
Avalia a capacidade do modelo de:
- Explicar trechos de código de forma clara e precisa
- Descrever o fluxo lógico e a estrutura do código
- Identificar padrões, algoritmos e estruturas importantes
- Interpretar a intenção do programador e o propósito do código

#### 2. Geração de Código
Avalia a habilidade de:
- Criar implementações completas ou parciais a partir de especificações
- Utilizar boas práticas de programação e padrões de projeto
- Seguir requisitos detalhados e restrições técnicas
- Gerar código limpo, eficiente, funcional e bem documentado

#### 3. Análise e Correção de Erros
Avalia a capacidade de:
- Localizar bugs, inconsistências e problemas lógicos
- Justificar tecnicamente os problemas identificados
- Propor correções adequadas e funcionais
- Sugerir melhorias estruturais e otimizações

### Estrutura Experimental
- **Total de prompts**: 18 (6 por categoria)
- **Modelos testados**: 2 (ChatGPT e Gemini)
- **Total de respostas coletadas**: 36
- **Métricas coletadas**: Tempo de resposta e consumo de tokens

## Estrutura do Projeto

```
TCC_Code/
│
├── Avaliacao Feita.xlsx         # Consolidação dos resultados das avaliações
├── chatgpt/                    # Scripts e respostas do ChatGPT
│   ├── codes/                  # Scripts Python para gerar respostas
│   │   ├── code_comprehension.py
│   │   ├── code_generation.py
│   │   └── error_analysis.py
│   └── responses/              # Respostas geradas pelo ChatGPT
│       ├── code_comprehension/
│       ├── code_generation/
│       └── error_analysis/
│
├── gemini/                     # Scripts e respostas do Gemini
│   ├── codes/                  # Scripts Python para gerar respostas
│   │   ├── code_comprehension.py
│   │   ├── code_generation.py
│   │   └── error_analysis.py
│   └── responses/              # Respostas geradas pelo Gemini
│       ├── code_comprehension/
│       ├── code_generation/
│       └── error_analysis/
│
├── prompts/                    # Prompts de entrada para avaliação
│   ├── code_comprehension/     # 6 prompts de compreensão
│   ├── code_generation/        # 6 prompts de geração
│   └── error_analysis/         # 6 prompts de análise de erros
│
├── requirements.txt            # Dependências do projeto
└── README.md                   # Este arquivo e documentação do estudo
```

## Arquivo de Consolidação de Resultados: `Avaliacao Feita.xlsx`

O arquivo `Avaliacao Feita.xlsx` reúne, em formato tabular, os principais resultados obtidos nos experimentos realizados com os modelos **ChatGPT (GPT-4.1-mini)** e **Gemini (Gemini 2.5 Flash)**. Ele funciona como a base quantitativa da análise apresentada no TCC, permitindo a verificação transparente dos dados utilizados nas comparações entre os modelos.

De forma geral, o arquivo está organizado para refletir a metodologia descrita neste repositório, contemplando:
- **Identificação do modelo e da categoria de tarefa** (compreensão de código, geração de código e análise/correção de erros)
- **Referência ao prompt utilizado** em cada experimento
- **Métricas objetivas** coletadas (como tempo de resposta e consumo de tokens)
- **Campos para avaliação qualitativa** da resposta, como qualidade técnica, clareza, completude e aderência ao enunciado

Esse documento eletrônico é utilizado como fonte para a elaboração de tabelas, gráficos e discussões presentes no texto final do TCC. Dessa forma, ele subsidia a análise comparativa, garante rastreabilidade entre as respostas dos modelos e os resultados apresentados e facilita a reprodução ou extensão do estudo por outros pesquisadores.

## Instalação e Configuração

### Pré-requisitos
- Python 3.7 ou superior
- Contas e chaves de API para:
  - OpenAI (ChatGPT)
  - Google Generative AI (Gemini)

### Passos para Instalação

1. **Clone o repositório** (ou baixe os arquivos do projeto)

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente**:
   
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   OPEN_AI_KEY=sua_chave_openai_aqui
   GOOGLE_API_KEY=sua_chave_google_aqui
   ```

4. **Execute os scripts de coleta de dados**:
   
   Para ChatGPT:
   ```bash
   cd chatgpt/codes
   python code_comprehension.py
   python code_generation.py
   python error_analysis.py
   ```
   
   Para Gemini:
   ```bash
   cd gemini/codes
   python code_comprehension.py
   python code_generation.py
   python error_analysis.py
   ```

## Métricas Coletadas

Cada resposta gerada inclui as seguintes métricas:
- **Tempo de resposta**: Medido em segundos desde o envio da requisição até a recepção da resposta
- **Tokens utilizados**: Quantidade total de tokens consumidos na requisição (incluindo prompt e resposta)

Essas métricas são automaticamente anexadas ao final de cada arquivo de resposta para análise posterior.

## Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação principal
- **OpenAI API**: Integração com ChatGPT (GPT-4.1-mini)
- **Google Generative AI SDK**: Integração com Gemini (Gemini 2.5 Flash)
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **requests**: Biblioteca para requisições HTTP (ChatGPT)

## Formato das Respostas

As respostas são salvas em arquivos Markdown (`.md`) com a seguinte nomenclatura:
- ChatGPT: `response_chatgpt_{número}.md`
- Gemini: `response_gemini_{número}.md`

Cada arquivo contém:
1. A resposta completa do modelo
2. Tempo de processamento (em segundos)
3. Quantidade de tokens utilizados

## Análise dos Resultados

Os resultados coletados permitem realizar análises comparativas em múltiplas dimensões:
- **Qualidade técnica**: Precisão e completude das respostas
- **Consistência**: Variação de qualidade entre diferentes prompts
- **Eficiência**: Tempo de resposta e consumo de recursos
- **Adequação**: Capacidade de atender requisitos específicos de cada categoria

## Considerações Finais

Este projeto fornece uma base empírica para:
- Compreender as capacidades e limitações de LLMs em contexto de desenvolvimento de software
- Orientar desenvolvedores na escolha do modelo mais adequado para suas necessidades
- Identificar áreas de melhoria para futuras versões dos modelos
- Contribuir para o corpo de conhecimento sobre IA aplicada à engenharia de software

## Autores

Eduardo karpfenstein, Giovani Furigo Finazzi, Luca Felipe de Lima Delmondes, Marcos Vinicius Correia Sanches

Instituto Nacional de Telecomunicações – Inatel
2025

---

**Nota**: Este projeto foi desenvolvido como parte do Trabalho de Conclusão de Curso. Para mais informações sobre a metodologia e resultados detalhados, consulte o documento completo do TCC.
