# Retenção e Recuperação de Clientes (Caso XP)

Projeto de análise de dados que simula um problema real do mercado financeiro: identificar sinais de risco de evasão de clientes antes que a saída aconteça, cruzando comportamento financeiro e histórico de atendimento.

## Contexto de Mercado

No fim de 2025, o setor financeiro brasileiro viveu um movimento de queda em métricas de satisfação de clientes, refletido em relatórios de balanço de grandes corretoras: episódios como os casos Americanas, Braskem e a liquidação do Banco Master afetaram diretamente a confiança de parte da base de clientes de investimento. O NPS (Net Promoter Score), métrica que mede a probabilidade de um cliente recomendar a empresa, recuou de forma expressiva nesse período. Historicamente, o mercado tratava essa métrica como um indicador de vaidade, reportado a cada trimestre sem ação prática associada. Este projeto nasce dessa dor real: transformar sinais de comportamento do cliente (saldo, movimentação, reclamações, satisfação) em um alerta de risco de evasão antes que o cliente efetivamente saia, permitindo que o time de relacionamento aja a tempo.

## Objetivo Técnico

Construir um pipeline de dados que centraliza informações de duas naturezas diferentes, comportamento financeiro e histórico de atendimento, e aplica regras de negócio para identificar clientes de alto valor com sinais de insatisfação, mesmo quando esses sinais não são óbvios (ex: cliente que nunca abriu uma reclamação formal).

## Arquitetura do Pipeline

Duas fontes são geradas separadamente, simulando dois sistemas diferentes de uma empresa real (um sistema de investimentos e um sistema de CRM/suporte): `comportamento_financeiro` e `historico_atendimento`. Ambas passam por um pipeline em Python que faz o merge pelo `ID` do cliente e aplica as regras de limpeza, e o resultado final é persistido na tabela `analytics_retencao`, no SQLite.

![Arquitetura do Pipeline](imagens/arquitetura-pipeline.png)

## Fontes de Dados e Campos

**`comportamento_financeiro`**
- `ID`
- `Segmento` (Varejo, Alta Renda, Private)
- `Saldo_Investido`
- `Qtd_Transacoes_Mes`
- `Data_Ultima_Transacao`

**`historico_atendimento`**
- `ID`
- `Qtd_Reclamacoes`
- `Nota_NPS`

## Regras de Limpeza Aplicadas

- **Nota de satisfação ausente:** em vez de descartar o cliente, a nota é substituída pela média das notas válidas da base, para não perder o cliente da análise.
- **Saldo investido igual a zero:** tratado de forma diferenciada usando a data da última transação. Um saldo zerado sem nenhum histórico de transação é considerado erro de sistema (cliente descartado). Um saldo zerado com transação registrada no passado é mantido como sinal real de evasão em andamento.

## Lógica de Identificação de Risco

A identificação usa subqueries correlacionadas em SQL, comparando cada cliente com a média do seu próprio segmento (não a média geral da base), já que o que é "alto" ou "baixo" varia por perfil de cliente. Três perfis de risco foram definidos:

1. **Saldo zerado com reclamação:** saldo investido igual a zero, ao menos uma reclamação aberta, e nota de satisfação abaixo da média do segmento.
2. **Cliente silencioso, valioso e insatisfeito:** saldo acima da média do segmento, nota abaixo da média do segmento, mas nenhuma reclamação formal registrada.
3. **Cliente valioso em queda de engajamento:** saldo acima da média do segmento, número de transações no mês abaixo da média do segmento, nota abaixo da média do segmento, sem reclamação formal.

## Resultados Encontrados

Em uma base de 200 clientes simulados, a consulta identificou 11 clientes de risco (~5,5% da base), uma proporção consistente com o esperado para um sistema de alerta (nem excessivo, nem irrelevante).

## Tecnologias Utilizadas

- Python (geração e tratamento de dados)
- SQLite (persistência e consultas analíticas)
- SQL (subqueries correlacionadas)

## Próximos Passos

- Dashboard em Power BI para visualização dos clientes de risco identificados
