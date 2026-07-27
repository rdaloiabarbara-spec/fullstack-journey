-- Query preparada para alimentar o dashboard (Power BI).
-- Diferente de clientes_risco.sql, esta retorna TODOS os clientes da base
-- (não só os de risco), com duas colunas categóricas:
--   Perfil_Risco: qual regra específica foi acionada (1, 2, 3 ou NULL)
--   Tipo_Acao: a natureza da ação recomendada (Corretiva, Preventiva, Sem risco)

WITH risco AS (
    SELECT
        c.ID,
        c.Segmento,
        c.Saldo_Investido,
        c.Qtd_Transacoes_Mes,
        c.Qtd_Reclamacoes,
        c.Nota_NPS,
        CASE
            -- Perfil 1: saldo zerado + reclamação + nota abaixo da média do segmento
            -- (nunca compete com 2 ou 3: saldo=0 não pode ser > média de um segmento,
            -- já que o saldo nunca é negativo)
            WHEN c.Saldo_Investido = 0
                 AND c.Qtd_Reclamacoes > 0
                 AND c.Nota_NPS < (
                     SELECT AVG(c2.Nota_NPS) FROM analytics_retencao c2
                     WHERE c2.Segmento = c.Segmento
                 )
            THEN 1

            -- Perfil 3 antes do 2: prioridade para quem soma o sinal de baixa movimentação
            -- >>> INVERTA ESTA ORDEM COM O BLOCO DO PERFIL 2 SE DISCORDAR DO CRITÉRIO <<<
            WHEN c.Qtd_Reclamacoes = 0
                 AND c.Saldo_Investido > (
                     SELECT AVG(c2.Saldo_Investido) FROM analytics_retencao c2
                     WHERE c2.Segmento = c.Segmento
                 )
                 AND c.Qtd_Transacoes_Mes < (
                     SELECT AVG(c2.Qtd_Transacoes_Mes) FROM analytics_retencao c2
                     WHERE c2.Segmento = c.Segmento
                 )
                 AND c.Nota_NPS < (
                     SELECT AVG(c2.Nota_NPS) FROM analytics_retencao c2
                     WHERE c2.Segmento = c.Segmento
                 )
            THEN 3

            -- Perfil 2: saldo alto + nota baixa + sem reclamação (sem exigir queda de transações)
            WHEN c.Qtd_Reclamacoes = 0
                 AND c.Saldo_Investido > (
                     SELECT AVG(c2.Saldo_Investido) FROM analytics_retencao c2
                     WHERE c2.Segmento = c.Segmento
                 )
                 AND c.Nota_NPS < (
                     SELECT AVG(c2.Nota_NPS) FROM analytics_retencao c2
                     WHERE c2.Segmento = c.Segmento
                 )
            THEN 2

            ELSE NULL
        END AS Perfil_Risco
    FROM analytics_retencao AS c
)
SELECT
    *,
    CASE
        WHEN Perfil_Risco = 1 THEN 'Corretiva'
        WHEN Perfil_Risco IN (2, 3) THEN 'Preventiva'
        ELSE 'Sem risco'
    END AS Tipo_Acao
FROM risco;