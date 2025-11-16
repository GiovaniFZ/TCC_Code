# Trabalho de Conclusão de Curso (TCC): Análise Comparativa de Desempenho de Grandes Modelos de Linguagem no Suporte ao Desenvolvimento de Software

## Introdução
O objetivo deste projeto é comparar o desempenho de diferentes LLMs (Large Language Models) em tarefas envolvendo código-fonte de linguagens amplamente utilizadas na engenharia de software, contemplando aspectos fundamentais na área. Cada critério possui 6 prompts específicos, enviados aos modelos **ChatGPT** e **Gemini**, permitindo uma comparação estruturada de suas capacidades, limitações, consistência e precisão técnica.

## Critérios
### 1. Compreensão de Código
Avalia a capacidade do modelo de:
- Explicar trechos de código
- Descrever o fluxo lógico
- Identificar estruturas importantes
- Interpretar a intenção do programador

### 2. Geração de Código
Avalia a habilidade de:
- Criar implementações completas ou parciais
- Utilizar boas práticas e padrões de projeto
- Seguir requisitos detalhados
- Gerar código limpo, eficiente e funcional

### 3. Análise e Correção de Erros
O modelo deve:
- Localizar bugs e inconsistências
- Justificar os problemas encontrados
- Propor correções adequadas
- Sugerir melhorias estruturais

## Estrutura
- `modelo/`
	- `codes/`: Arquivos Python para gerar as respostas dos prompts
	- `responses/`: Respostas geradas pelo modelo, em relação a cada categoria.

- `prompts/`: prompts de entrada usados para a avaliação, organizados por categoria.
- `requirements.txt`: lista de dependências do projeto (use `pip install -r requirements.txt`).







