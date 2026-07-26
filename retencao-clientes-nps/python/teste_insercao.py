import sqlite3
import os

pasta_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(pasta_atual, "..", "data", "retencao.db")

conexao = sqlite3.connect(caminho_banco)
conexao.execute("""
    INSERT OR REPLACE INTO analytics_retencao 
    (ID, Segmento, Saldo_Investido, Qtd_Transacoes_Mes, Data_Ultima_Transacao, Qtd_Reclamacoes, Nota_NPS)
    VALUES (996, 'Varejo', 999, 2, '2026-01-01', 0, 0)
""")
conexao.commit()
conexao.close()
print("cliente teste inserido")