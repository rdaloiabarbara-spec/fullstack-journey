import random
from datetime import datetime, timedelta
import sqlite3
import os

def gerar_comportamento_financeiro(quantidade, proporcao_saldo_zerado=0.05):
    lista_clientes = []
    for i in range(quantidade):
        # Sem isso, Saldo_Investido = 0 é praticamente impossível de sair de um
        # randint(0, 50000) — e o Perfil 1 (saldo zerado) nunca teria dados para
        # testar. Aqui forçamos uma proporção pequena e intencional desse cenário.
        forcar_saldo_zerado = random.random() < proporcao_saldo_zerado

        if forcar_saldo_zerado:
            saldo = 0
            # Transação passada garantida: representa evasão real em andamento,
            # não erro de sistema — mantém coerência com a regra de limpeza
            # que descarta saldo zero SEM histórico de transação.
            dias_atras = random.randint(1, 365)
            data_transacao = (datetime.now() - timedelta(days=dias_atras)).date()
        else:
            # Começa em 1, não em 0: o zero já é tratado explicitamente acima,
            # então aqui ele não pode reaparecer de forma não intencional.
            saldo = random.randint(1, 50000)
            tem_transacao = random.choice([True, False])
            if tem_transacao:
                dias_atras = random.randint(1, 365)
                data_transacao = (datetime.now() - timedelta(days=dias_atras)).date()
            else:
                data_transacao = None

        cliente = {
            "ID": i + 1,
            "Segmento": random.choice(["Varejo", "Alta Renda", "Private"]),
            "Saldo_Investido": saldo,
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

def criar_tabela_dashboard():
    # Separada de salvar_no_banco de propósito: essa função não gera nem limpa
    # dados novos, ela consome o que já está em analytics_retencao e aplica uma
    # regra de negócio (a lógica de risco) por cima. São responsabilidades
    # diferentes, por isso vivem em funções diferentes.
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_sql = os.path.join(pasta_atual, "..", "sql", "clientes_risco_dashboard.sql")
    caminho_banco = os.path.join(pasta_atual, "..", "data", "retencao.db")

    with open(caminho_sql, "r", encoding="utf-8") as arquivo:
        query = arquivo.read()

    # remove o ";" final: precisamos embutir a query como subconsulta de um
    # CREATE TABLE, e um ";" no meio do caminho quebraria a sintaxe
    query = query.strip().rstrip(";")

    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    # DROP antes do CREATE: garante que rodar o script de novo sempre gere uma
    # versão atualizada da tabela, em vez de falhar porque ela já existe
    cursor.execute("DROP TABLE IF EXISTS clientes_risco_dashboard")
    cursor.execute(f"CREATE TABLE clientes_risco_dashboard AS {query}")

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    # Semente fixa: garante que qualquer pessoa que rodar este script gere
    # exatamente a mesma base fictícia documentada no README — reprodutibilidade,
    # não dinamismo de dados reais (que este projeto não simula).
    random.seed(42)

    fin = gerar_comportamento_financeiro(200)
    ate = gerar_historico_atendimento(200)
    completo = unir_dados(fin, ate)
    limpo = limpar_dados(completo)
    salvar_no_banco(limpo)
    criar_tabela_dashboard()
    print("Dados salvos com sucesso!")