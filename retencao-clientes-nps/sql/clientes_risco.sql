SELECT ID, Segmento, Saldo_Investido, Qtd_Transacoes_Mes, Qtd_Reclamacoes, Nota_NPS
FROM analytics_retencao AS c
WHERE
  -- Perfil 1: saldo zerado, reclamação, nota baixa
  (c.Saldo_Investido = 0
   AND c.Qtd_Reclamacoes > 0
   AND c.Nota_NPS < (SELECT AVG(c2.Nota_NPS) FROM analytics_retencao AS c2 WHERE c2.Segmento = c.Segmento))

  OR

  -- Perfil 2: saldo alto, nota baixa, sem reclamação
  (c.Qtd_Reclamacoes = 0
   AND c.Saldo_Investido > (SELECT AVG(c2.Saldo_Investido) FROM analytics_retencao AS c2 WHERE c2.Segmento = c.Segmento)
   AND c.Nota_NPS < (SELECT AVG(c2.Nota_NPS) FROM analytics_retencao AS c2 WHERE c2.Segmento = c.Segmento))

  OR

  -- Perfil 3: saldo alto, pouca movimentação, sem reclamação, nota baixa
  (c.Qtd_Reclamacoes = 0
   AND c.Saldo_Investido > (SELECT AVG(c2.Saldo_Investido) FROM analytics_retencao AS c2 WHERE c2.Segmento = c.Segmento)
   AND c.Qtd_Transacoes_Mes < (SELECT AVG(c2.Qtd_Transacoes_Mes) FROM analytics_retencao AS c2 WHERE c2.Segmento = c.Segmento)
   AND c.Nota_NPS < (SELECT AVG(c2.Nota_NPS) FROM analytics_retencao AS c2 WHERE c2.Segmento = c.Segmento))
   