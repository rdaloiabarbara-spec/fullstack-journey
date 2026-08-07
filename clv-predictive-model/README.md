# Previsão de Customer Lifetime Value (CLV) com Machine Learning

Este repositório contém o projeto de MVP (Minimum Viable Product) desenvolvido para a **Sprint: Machine Learning e Analytics** do curso de Pós-Graduação em Ciência de Dados e Analytics da **PUC-Rio**.

---

## 🎯 Objetivo do Projeto
O objetivo principal é construir um pipeline preditivo de ponta a ponta utilizando modelos de regressão avançados para estimar o valor financeiro de longo prazo (**Customer Lifetime Value - LTV**) que um cliente gerará para a empresa no seu segundo ano de relacionamento, baseando-se estritamente no seu comportamento transacional do primeiro ano.

No contexto de negócios, essa previsão apoia decisões estratégicas de alto impacto, como:
* Otimização do orçamento de Aquisição de Clientes (**CAC**).
* Alocação de capital em campanhas de retenção no ecossistema de CRM.
* Identificação precoce de clientes da cauda longa de altíssimo valor (atacadistas/corporativos).

---

## 📊 Dataset Utilizado
O projeto utiliza o conjunto de dados históricos **Online Retail II**, contendo o registro de transações brutas linha por linha. 

A partir desses logs originais de compras, foi realizada a agregação de atributos comportamentais robustos por cliente (`Customer ID`) seguindo a lógica de **RFM (Recência, Frequência e Valor Monetário)** para alimentar os modelos supervisionados, simulando os desafios reais de manipulação de dados encontrados em Data Lakes corporativos do varejo.

---

## 🏆 Resultados Obtidos (Performance dos Modelos)

O projeto aplicou uma escada de complexidade rigorosa, avaliando os modelos em dados de teste completamente inéditos. A **Random Forest Otimizada** consagrou-se como a solução campeã:

| Modelo | Métrica Principal ($R^2$) | Outras Métricas (MAE / RMSE) | Status do Modelo |
| :--- | :---: | :---: | :--- |
| **Baseline** (Dummy Mediana) | -0.0277 | MAE: 174.61 / RMSE: 1054.95 | Descartado (Incapaz de prever grandes compradores) |
| **Modelo 1** (Regressão Ridge) | 0.6945 | MAE: 334.08 / RMSE: 575.22 | Descartado (Subajuste/Underfitting severo) |
| **Modelo 2** (Random Forest Inicial) | 0.9206 | MAE: 146.60 / RMSE: 293.23 | Ótimo desempenho inicial |
| **Modelo Otimizado (RF Otimizada)** | **0.9492** | **MAE: 124.15 / RMSE: 234.44** | **Campeão (Selecionado para Produção)** |

> 📌 **Significado Prático:** O modelo final é capaz de explicar **94.92%** da variabilidade do faturamento futuro de novos clientes, operando com um erro médio absoluto (MAE) de apenas \$124.15 por cliente.

---

## 🛠️ Estrutura Técnica do MVP
O fluxo de desenvolvimento no Google Colab foi projetado seguindo as diretrizes de reprodutibilidade e boas práticas de engenharia de machine learning:

1. **Definição do Problema e Hipóteses:** Justificativa do uso de abordagens não-lineares frente à assimetria dos dados financeiros.
2. **Preparação de Dados e Engenharia de Atributos:** Separação estrita dos dados em treino e teste realizada *antes* de qualquer transformação para garantir a mitigação absoluta de vazamento de dados (*data leakage*).
3. **Pipeline Automatizado:** Uso do `Pipeline` do Scikit-Learn integrando passos de imputação e padronização (Z-score).
4. **Otimização Estocástica:** Ajuste fino de hiperparâmetros via `RandomizedSearchCV` com validação cruzada `KFold (n_splits=5)` para mitigar o sobreajuste (*overfitting*).
5. **Governança:** Análise de diagnóstico de resíduos (heterocedasticidade) e persistência do artefato final (`modelo_final.pkl`) via `joblib`.

---

## 🚀 Como Executar

1. Abra o arquivo `.ipynb` presente neste repositório.
2. O conjunto de dados bruto está configurado para carregar de forma 100% automatizada e direta a partir do endereço público em formato `raw` do GitHub, garantindo que o código execute do início ao fim sem dependências locais na máquina do avaliador.
3. No menu superior do seu ambiente de execução, selecione a opção **Reiniciar e executar tudo** (Run All).
