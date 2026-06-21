"""
Cria um banco de dados SQLite a partir dos CSVs gerados,
estruturando as tabelas com relacionamentos (chaves primárias/estrangeiras).
"""

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "ecommerce.db")

# Remove banco antigo, se existir, para gerar do zero
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ---------------------------------------------------------
# Criação das tabelas
# ---------------------------------------------------------
cursor.executescript("""
CREATE TABLE produtos (
    produto_id INTEGER PRIMARY KEY,
    nome_produto TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco_unitario REAL NOT NULL
);

CREATE TABLE clientes (
    cliente_id INTEGER PRIMARY KEY,
    regiao TEXT NOT NULL,
    cidade TEXT NOT NULL
);

CREATE TABLE pedidos (
    pedido_id INTEGER PRIMARY KEY,
    data_pedido TEXT NOT NULL,
    cliente_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_unitario REAL NOT NULL,
    desconto_pct REAL NOT NULL,
    valor_total REAL NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes (cliente_id),
    FOREIGN KEY (produto_id) REFERENCES produtos (produto_id)
);
""")

# ---------------------------------------------------------
# Carrega os CSVs para as tabelas
# ---------------------------------------------------------
base_dir = os.path.dirname(__file__)
df_produtos = pd.read_csv(os.path.join(base_dir, "produtos.csv"))
df_clientes = pd.read_csv(os.path.join(base_dir, "clientes.csv"))
df_pedidos = pd.read_csv(os.path.join(base_dir, "pedidos.csv"))

df_produtos.to_sql("produtos", conn, if_exists="append", index=False)
df_clientes.to_sql("clientes", conn, if_exists="append", index=False)
df_pedidos.to_sql("pedidos", conn, if_exists="append", index=False)

conn.commit()

# Validação rápida
cursor.execute("SELECT COUNT(*) FROM pedidos")
total_pedidos = cursor.fetchone()[0]
print(f"Banco criado com sucesso em: {DB_PATH}")
print(f"Total de pedidos carregados: {total_pedidos}")

conn.close()
