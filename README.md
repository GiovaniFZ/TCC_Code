# Trabalho de Conclusão de Curso (TCC) sobre Análise Comparativa entre Modelos de Inteligência Artificial
Avaliação entre ChatGPT e Gemini aplicados à engenharia de software 

## 1. Introdução
O objetivo deste projeto — parte integrante do Trabalho de Conclusão de Curso — é comparar o desempenho de diferentes LLMs (Large Language Models) em tarefas envolvendo código-fonte de linguagens amplamente utilizadas na engenharia de software.

A análise contempla três eixos fundamentais:

Compreensão de código

Geração de código

Análise e correção de erros

Cada eixo possui 6 prompts específicos, enviados aos modelos ChatGPT e Gemini, permitindo uma comparação estruturada de suas capacidades, limitações, consistência e precisão técnica.


🤖 ChatGPT vs Gemini
Um estudo comparativo baseado em qualidade, precisão e utilidade prática

🚀 Compreensão • Geração • Depuração de Código

## Sobre o Projeto

Este projeto automatiza a execução de prompts para ambos os modelos e captura suas respostas em formato Markdown, permitindo:

Avaliação qualitativa (clareza, precisão, organização)

Avaliação técnica (correção lógica e sintática)

Avaliação comparativa (vantagens e limitações lado a lado)

## Categorias de Análise
### 1. Compreensão de Código

Avalia a capacidade do modelo de:

Explicar trechos de código

Descrever o fluxo lógico

Identificar estruturas importantes

Interpretar a intenção do programador

Inclui 6 prompts exclusivos

### 2. Geração de Código

Avalia a habilidade de:

Criar implementações completas ou parciais

Utilizar boas práticas e padrões de projeto

Seguir requisitos detalhados

Gerar código limpo, eficiente e funcional

Inclui 6 prompts exclusivos

### 3. Análise e Correção de Erros

O modelo deve:

Localizar bugs e inconsistências

Justificar os problemas encontrados

Propor correções adequadas

Sugerir melhorias estruturais

Inclui 6 prompts exclusivos

### Como Executar as Análises
1. Instalar dependências
pip install -r requirements.txt

2. Executar as categorias
# Compreensão de código
python codes/code_comprehension.py

# Geração de código
python codes/code_generation.py

# Análise de erros
python codes/error_analysis.py

## Modelos Suportados
Modelo	Diretório das Respostas
ChatGPT	responses/chatgpt/
Gemini	responses/gemini/

As respostas são armazenadas automaticamente em Markdown para facilitar leitura e análise comparativa.

Padrão dos Arquivos de Resposta

Todos os arquivos seguem a convenção:

response_[modelo]_[número].md


Exemplo:

response_chatgpt_1.md


Cada arquivo contém:

O prompt avaliado

A resposta completa

Marcação por categoria e modelo






