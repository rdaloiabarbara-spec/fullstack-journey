SELECT ID, Segmento, Saldo_Investido, Qtd_Reclamacoes, Nota_NPS
FROM analytics_retencao AS c
WHERE c.Qtd_Reclamacoes = 0
  AND c.Saldo_Investido > (
      SELECT AVG(c2.Saldo_Investido)
      FROM analytics_retencao AS c2
      WHERE c2.Segmento = c.Segmento
  )
  AND c.Nota_NPS < (
      SELECT AVG(c2.Nota_NPS)
      FROM analytics_retencao AS c2
      WHERE c2.Segmento = c.Segmento
  )