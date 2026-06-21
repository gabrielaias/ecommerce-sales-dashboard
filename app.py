"""
Dashboard de Análise de Vendas — E-commerce
Desenvolvido com Streamlit + SQL (SQLite) + Plotly.

Para executar localmente:
    streamlit run app.py
"""

import os
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Vendas | E-commerce",
    page_icon="📊",
    layout="wide",
)

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "ecommerce.db")


@st.cache_data
def carregar_dados():
    """Carrega os dados do banco SQLite via queries SQL."""
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            p.pedido_id,
            p.data_pedido,
            p.quantidade,
            p.valor_unitario,
            p.desconto_pct,
            p.valor_total,
            p.status,
            c.regiao,
            c.cidade,
            pr.nome_produto,
            pr.categoria
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.cliente_id
        JOIN produtos pr ON p.produto_id = pr.produto_id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    df["data_pedido"] = pd.to_datetime(df["data_pedido"])
    df["ano_mes"] = df["data_pedido"].dt.to_period("M").astype(str)
    return df


df = carregar_dados()

# ---------------------------------------------------------
# Sidebar — Filtros
# ---------------------------------------------------------
st.sidebar.header("🔍 Filtros")

data_min = df["data_pedido"].min().date()
data_max = df["data_pedido"].max().date()

intervalo_datas = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max,
)

regioes_disponiveis = sorted(df["regiao"].unique())
regioes_selecionadas = st.sidebar.multiselect(
    "Região", options=regioes_disponiveis, default=regioes_disponiveis
)

categorias_disponiveis = sorted(df["categoria"].unique())
categorias_selecionadas = st.sidebar.multiselect(
    "Categoria", options=categorias_disponiveis, default=categorias_disponiveis
)

status_disponiveis = sorted(df["status"].unique())
status_selecionados = st.sidebar.multiselect(
    "Status do pedido", options=status_disponiveis, default=status_disponiveis
)

# Aplicar filtros
if len(intervalo_datas) == 2:
    data_inicio_filtro, data_fim_filtro = intervalo_datas
else:
    data_inicio_filtro, data_fim_filtro = data_min, data_max

df_filtrado = df[
    (df["data_pedido"].dt.date >= data_inicio_filtro)
    & (df["data_pedido"].dt.date <= data_fim_filtro)
    & (df["regiao"].isin(regioes_selecionadas))
    & (df["categoria"].isin(categorias_selecionadas))
    & (df["status"].isin(status_selecionados))
]

# ---------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------
st.title("📊 Dashboard de Análise de Vendas")
st.markdown("Visão geral de performance de vendas, por período, categoria e região.")

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------
df_entregue = df_filtrado[df_filtrado["status"] != "Cancelado"]

faturamento_total = df_entregue["valor_total"].sum()
ticket_medio = df_entregue["valor_total"].mean()
total_pedidos = df_entregue["pedido_id"].nunique()
taxa_cancelamento = (
    df_filtrado[df_filtrado["status"] == "Cancelado"]["pedido_id"].nunique()
    / df_filtrado["pedido_id"].nunique()
    * 100
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}")
col2.metric("🧾 Ticket Médio", f"R$ {ticket_medio:,.2f}")
col3.metric("📦 Total de Pedidos", f"{total_pedidos:,}")
col4.metric("❌ Taxa de Cancelamento", f"{taxa_cancelamento:.1f}%")

st.divider()

# ---------------------------------------------------------
# Gráficos
# ---------------------------------------------------------
col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("Faturamento por Mês")
    df_mes = (
        df_entregue.groupby("ano_mes")["valor_total"]
        .sum()
        .reset_index()
        .sort_values("ano_mes")
    )
    fig_mes = px.line(
        df_mes, x="ano_mes", y="valor_total", markers=True,
        labels={"ano_mes": "Mês", "valor_total": "Faturamento (R$)"},
    )
    fig_mes.update_layout(margin=dict(t=10))
    st.plotly_chart(fig_mes, use_container_width=True)

with col_dir:
    st.subheader("Faturamento por Categoria")
    df_categoria = (
        df_entregue.groupby("categoria")["valor_total"]
        .sum()
        .reset_index()
        .sort_values("valor_total", ascending=False)
    )
    fig_categoria = px.bar(
        df_categoria, x="categoria", y="valor_total",
        labels={"categoria": "Categoria", "valor_total": "Faturamento (R$)"},
        color="categoria",
    )
    fig_categoria.update_layout(showlegend=False, margin=dict(t=10))
    st.plotly_chart(fig_categoria, use_container_width=True)

col_esq2, col_dir2 = st.columns(2)

with col_esq2:
    st.subheader("Faturamento por Região")
    df_regiao = (
        df_entregue.groupby("regiao")["valor_total"]
        .sum()
        .reset_index()
        .sort_values("valor_total", ascending=False)
    )
    fig_regiao = px.pie(
        df_regiao, names="regiao", values="valor_total", hole=0.45,
    )
    fig_regiao.update_layout(margin=dict(t=10))
    st.plotly_chart(fig_regiao, use_container_width=True)

with col_dir2:
    st.subheader("Top 10 Produtos Mais Vendidos")
    df_top_produtos = (
        df_entregue.groupby("nome_produto")["valor_total"]
        .sum()
        .reset_index()
        .sort_values("valor_total", ascending=False)
        .head(10)
    )
    fig_top = px.bar(
        df_top_produtos.sort_values("valor_total"),
        x="valor_total", y="nome_produto", orientation="h",
        labels={"nome_produto": "Produto", "valor_total": "Faturamento (R$)"},
    )
    fig_top.update_layout(margin=dict(t=10))
    st.plotly_chart(fig_top, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# Tabela detalhada
# ---------------------------------------------------------
with st.expander("📋 Ver dados detalhados"):
    st.dataframe(
        df_filtrado[
            ["pedido_id", "data_pedido", "nome_produto", "categoria",
             "regiao", "cidade", "quantidade", "valor_total", "status"]
        ].sort_values("data_pedido", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

st.caption("Dados sintéticos gerados para fins de demonstração. Projeto desenvolvido por Gabriel.")
