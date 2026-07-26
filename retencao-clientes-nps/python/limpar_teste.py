import sqlite3
import os

pasta_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(pasta_atual, "..", "data", "retencao.db")

conexao = sqlite3.connect(caminho_banco)
conexao.execute("DELETE FROM analytics_retencao WHERE ID IN (998, 999, 997, 996)")
conexao.commit()
conexao.close()
print("clientes teste removidos")