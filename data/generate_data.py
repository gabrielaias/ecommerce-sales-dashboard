"""
Gera um dataset sintético e realista de vendas de e-commerce.
Inclui: clientes, produtos e pedidos, com sazonalidade e variação por região.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ---------------------------------------------------------
# 1. Produtos
# ---------------------------------------------------------
categorias = {
    "Eletrônicos": ["Fone de Ouvido", "Smartwatch", "Carregador Portátil", "Caixa de Som", "Mouse Gamer"],
    "Moda": ["Camiseta", "Tênis Casual", "Jaqueta Jeans", "Boné", "Mochila"],
    "Casa & Decoração": ["Luminária LED", "Organizador Multiuso", "Jogo de Panelas", "Tapete", "Vaso Decorativo"],
    "Beleza": ["Kit Skincare", "Perfume", "Secador de Cabelo", "Kit Maquiagem", "Hidratante Corporal"],
    "Esporte": ["Tênis de Corrida", "Garrafa Térmica", "Kit Halteres", "Bicicleta Ergométrica", "Tapete de Yoga"],
}

produtos = []
produto_id = 1
preco_base = {
    "Eletrônicos": (80, 450),
    "Moda": (40, 220),
    "Casa & Decoração": (30, 180),
    "Beleza": (25, 150),
    "Esporte": (50, 900),
}

for categoria, itens in categorias.items():
    for item in itens:
        preco_min, preco_max = preco_base[categoria]
        produtos.append({
            "produto_id": produto_id,
            "nome_produto": item,
            "categoria": categoria,
            "preco_unitario": round(np.random.uniform(preco_min, preco_max), 2),
        })
        produto_id += 1

df_produtos = pd.DataFrame(produtos)

# ---------------------------------------------------------
# 2. Clientes
# ---------------------------------------------------------
regioes = {
    "Sudeste": ["São Paulo", "Rio de Janeiro", "Belo Horizonte"],
    "Sul": ["Curitiba", "Porto Alegre", "Florianópolis"],
    "Nordeste": ["Salvador", "Recife", "Fortaleza"],
    "Centro-Oeste": ["Brasília", "Goiânia", "Campo Grande"],
    "Norte": ["Manaus", "Belém"],
}

n_clientes = 500
clientes = []
for cliente_id in range(1, n_clientes + 1):
    regiao = np.random.choice(
        list(regioes.keys()), p=[0.42, 0.22, 0.20, 0.11, 0.05]
    )
    cidade = np.random.choice(regioes[regiao])
    clientes.append({
        "cliente_id": cliente_id,
        "regiao": regiao,
        "cidade": cidade,
    })

df_clientes = pd.DataFrame(clientes)

# ---------------------------------------------------------
# 3. Pedidos (com sazonalidade: Nov/Dez mais fortes - Black Friday/Natal)
# ---------------------------------------------------------
data_inicio = datetime(2024, 1, 1)
data_fim = datetime(2025, 12, 31)
dias_totais = (data_fim - data_inicio).days

n_pedidos = 6000
pedidos = []

# Peso de sazonalidade por mês (índice 1-12)
peso_mes = {
    1: 0.8, 2: 0.7, 3: 0.8, 4: 0.85, 5: 0.9, 6: 0.85,
    7: 0.8, 8: 0.85, 9: 0.9, 10: 1.1, 11: 1.6, 12: 1.5
}

# Gerar datas com peso de sazonalidade
datas_possiveis = [data_inicio + timedelta(days=i) for i in range(dias_totais + 1)]
pesos_datas = [peso_mes[d.month] for d in datas_possiveis]
pesos_datas = np.array(pesos_datas) / sum(pesos_datas)

datas_escolhidas = np.random.choice(datas_possiveis, size=n_pedidos, p=pesos_datas)

status_opcoes = ["Entregue", "Entregue", "Entregue", "Entregue", "Cancelado", "Em trânsito"]

for pedido_id in range(1, n_pedidos + 1):
    cliente = df_clientes.sample(1).iloc[0]
    produto = df_produtos.sample(1).iloc[0]
    quantidade = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.45, 0.2, 0.15, 0.1, 0.05, 0.05])
    desconto_pct = np.random.choice([0, 0, 0, 0.05, 0.10, 0.15], p=[0.5, 0.15, 0.1, 0.1, 0.1, 0.05])

    valor_unitario = produto["preco_unitario"]
    valor_total = round(valor_unitario * quantidade * (1 - desconto_pct), 2)

    pedidos.append({
        "pedido_id": pedido_id,
        "data_pedido": datas_escolhidas[pedido_id - 1].strftime("%Y-%m-%d"),
        "cliente_id": cliente["cliente_id"],
        "produto_id": produto["produto_id"],
        "quantidade": quantidade,
        "valor_unitario": valor_unitario,
        "desconto_pct": desconto_pct,
        "valor_total": valor_total,
        "status": np.random.choice(status_opcoes),
    })

df_pedidos = pd.DataFrame(pedidos)

# ---------------------------------------------------------
# 4. Salvar CSVs
# ---------------------------------------------------------
df_produtos.to_csv("data/produtos.csv", index=False)
df_clientes.to_csv("data/clientes.csv", index=False)
df_pedidos.to_csv("data/pedidos.csv", index=False)

print(f"Produtos gerados: {len(df_produtos)}")
print(f"Clientes gerados: {len(df_clientes)}")
print(f"Pedidos gerados: {len(df_pedidos)}")
print("Dataset salvo em data/produtos.csv, data/clientes.csv, data/pedidos.csv")
