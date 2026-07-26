import random
from datetime import datetime, timedelta
import sqlite3
import os

def gerar_comportamento_financeiro(quantidade):
    lista_clientes = []
    for i in range(quantidade):
        tem_transacao = random.choice([True, False])
        if tem_transacao:
            dias_atras = random.randint(1, 365)
            data_transacao = (datetime.now() - timedelta(days=dias_atras)).date()
        else:
            data_transacao = None

        cliente = {
            "ID": i + 1,
            "Segmento": random.choice(["Varejo", "Alta Renda", "Private"]),
            "Saldo_Investido": random.randint(0, 50000),
            "Qtd_Transacoes_Mes": random.randint(0, 20),
            "Data_Ultima_Transacao": data_transacao
        }
        lista_clientes.append(cliente)
    return lista_clientes

def gerar_historico_atendimento(quantidade):
    lista_clientes = []
    for i in range(quantidade):
        cliente = {
            "ID": i + 1,
            "Qtd_Reclamacoes": random.randint(0, 5),
            "Nota_NPS": random.choice([None, random.randint(0, 10)])
        }
        lista_clientes.append(cliente)
    return lista_clientes

def unir_dados(financeiro, atendimento):
    dados_unidos = []
    for cliente_fin in financeiro:
        for cliente_ate in atendimento:
            if cliente_fin["ID"] == cliente_ate["ID"]:
                cliente_completo = {
                    "ID": cliente_fin["ID"],
                    "Segmento": cliente_fin["Segmento"], 
                    "Saldo_Investido": cliente_fin["Saldo_Investido"],
                    "Qtd_Transacoes_Mes": cliente_fin["Qtd_Transacoes_Mes"],
                    "Data_Ultima_Transacao": cliente_fin["Data_Ultima_Transacao"],
                    "Qtd_Reclamacoes": cliente_ate["Qtd_Reclamacoes"],
                    "Nota_NPS": cliente_ate["Nota_NPS"]
                }
                dados_unidos.append(cliente_completo)
    return dados_unidos

def limpar_dados(dados):
    notas_validas = [c["Nota_NPS"] for c in dados if c["Nota_NPS"] is not None]

    if len(notas_validas) > 0:
        media_nps = sum(notas_validas) / len(notas_validas)
    else:
        media_nps = 5

    dados_limpos = []
    for cliente in dados:
        if cliente["Nota_NPS"] is None:
            cliente["Nota_NPS"] = round(media_nps, 1)

        saldo_zerado = cliente["Saldo_Investido"] == 0
        nunca_transacionou = cliente["Data_Ultima_Transacao"] is None

        if saldo_zerado and nunca_transacionou:
            continue  # descarta: provável erro de sistema, não é cliente real

        dados_limpos.append(cliente)

    return dados_limpos

def salvar_no_banco(dados):
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(pasta_atual, "..", "data", "retencao.db")
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics_retencao (
            ID INTEGER PRIMARY KEY,
            Segmento TEXT,
            Saldo_Investido INTEGER,
            Qtd_Transacoes_Mes INTEGER,
            Data_Ultima_Transacao TEXT,
            Qtd_Reclamacoes INTEGER,
            Nota_NPS REAL
            
        )
    """)

    for cliente in dados:
           cursor.execute("""
            INSERT OR REPLACE INTO analytics_retencao 
            (ID, Segmento, Saldo_Investido, Qtd_Transacoes_Mes, Data_Ultima_Transacao, Qtd_Reclamacoes, Nota_NPS)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            cliente["ID"],
            cliente["Segmento"],
            cliente["Saldo_Investido"],
            cliente["Qtd_Transacoes_Mes"],
            str(cliente["Data_Ultima_Transacao"]) if cliente["Data_Ultima_Transacao"] is not None else None,
            cliente["Qtd_Reclamacoes"],
            cliente["Nota_NPS"]
        ))

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    fin = gerar_comportamento_financeiro(20)
    ate = gerar_historico_atendimento(20)
    completo = unir_dados(fin, ate)
    limpo = limpar_dados(completo)
    salvar_no_banco(limpo)
    print("Dados salvos com sucesso!")

