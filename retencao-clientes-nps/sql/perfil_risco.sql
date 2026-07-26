SELECT ID, Segmento, Saldo_Investido, Qtd_Reclamacoes, Nota_NPS
FROM analytics_retencao AS c
WHERE c.Saldo_Investido = 0
  AND c.Qtd_Reclamacoes > 0
  AND c.Nota_NPS < (
      SELECT AVG(c2.Nota_NPS)
      FROM analytics_retencao AS c2
      WHERE c2.Segmento = c.Segmento
  )
