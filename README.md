# Análise de Qualidade de Repositórios Java

## Descrição

Este projeto visa analisar a qualidade de repositórios desenvolvidos na linguagem Java, correlacionando suas características de qualidade com o processo de desenvolvimento. Utilizando métricas de qualidade calculadas pela ferramenta CK, o objetivo é entender como fatores como popularidade, maturidade, atividade e tamanho impactam a qualidade do código em repositórios open-source.

## Objetivos

O laboratório tem como objetivo responder às seguintes questões de pesquisa:

- **RQ 01:** Qual a relação entre a popularidade dos repositórios e suas características de qualidade?
- **RQ 02:** Qual a relação entre a maturidade dos repositórios e suas características de qualidade?
- **RQ 03:** Qual a relação entre a atividade dos repositórios e suas características de qualidade?
- **RQ 04:** Qual a relação entre o tamanho dos repositórios e suas características de qualidade?

## Metodologia

1. **Seleção de Repositórios:**
   - Coleta dos 1.000 repositórios Java mais populares do GitHub.
   - Cálculo das métricas de qualidade e características de processo.

2. **Definição de Métricas:**
   - **Métricas de Processo:**
     - Popularidade: número de estrelas
     - Tamanho: linhas de código (LOC) e linhas de comentários
     - Atividade: número de releases
     - Maturidade: idade (em anos) dos repositórios
   - **Métricas de Qualidade:**
     - CBO: Coupling between objects
     - DIT: Depth Inheritance Tree
     - LCOM: Lack of Cohesion of Methods

3. **Coleta e Análise de Dados:**
   - Utilização das APIs REST do GitHub para coleta de dados.
   - Análise de métricas de qualidade com a ferramenta CK, gerando arquivos .csv para resultados.

## Resultados

Os resultados da análise serão sumarizados no Relatório para cada questão de pesquisa.
