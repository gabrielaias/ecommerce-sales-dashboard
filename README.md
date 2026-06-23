# 📊 Dashboard de Análise de Vendas — E-commerce

Dashboard interativo para análise de performance de vendas, desenvolvido com **Python, SQL e Streamlit**.

🔗 **Demo ao vivo**: [gabriel-sales-dashboard.streamlit.app](https://gabriel-sales-dashboard.streamlit.app)

## 📸 Preview

Adiciona screenshot do dashboard atualizado

## 💡 Sobre o projeto

Este projeto simula um cenário comum no e-commerce: a necessidade de **monitorar vendas, identificar tendências sazonais e tomar decisões baseadas em dados**, sem depender de planilhas manuais ou ferramentas pagas de BI.

O dashboard permite que qualquer gestor, sem conhecimento técnico, explore os dados de forma visual e interativa, filtrando por período, categoria, região e status do pedido.

### Problema de negócio resolvido

- Visibilidade rápida de KPIs essenciais (faturamento, ticket médio, taxa de cancelamento)
- Identificação de sazonalidade (picos em Black Friday e Natal)
- Comparação de performance entre categorias, produtos e regiões
- Base para decisões de estoque, marketing e precificação

> **Nota**: os dados utilizados são **sintéticos** (gerados artificialmente para fins de demonstração), mas a estrutura e a lógica são as mesmas aplicadas em dados reais de um cliente.

## 🛠️ Tecnologias utilizadas

- 🐍 **Python** — manipulação e processamento de dados
- 🗄️ **SQL (SQLite)** — modelagem relacional e consultas analíticas
- 📈 **Plotly** — visualizações interativas
- 🎈 **Streamlit** — construção do dashboard web

## 🗂️ Estrutura do projeto

```
ecommerce-sales-dashboard/
├── app.py                  # Aplicação principal (Streamlit)
├── data/
│   ├── generate_data.py    # Geração do dataset sintético
│   ├── create_db.py        # Criação do banco SQLite a partir dos CSVs
│   ├── produtos.csv
│   ├── clientes.csv
│   ├── pedidos.csv
│   └── ecommerce.db
├── requirements.txt
└── README.md
```

## ✨ Funcionalidades

- Filtros interativos por período, região, categoria e status do pedido
- KPIs em tempo real (faturamento, ticket médio, total de pedidos, taxa de cancelamento)
- Gráficos de tendência mensal, ranking de produtos, distribuição por região e categoria
- Tabela detalhada com todos os pedidos filtrados

## ▶️ Como executar localmente

```bash
# 1. Clone o repositório
git clone <URL_DO_REPOSITORIO>
cd ecommerce-sales-dashboard

# 2. Instale as dependências
pip install -r requirements.txt

# 3. (Opcional) Gere os dados novamente, caso queira customizar o dataset
python data/generate_data.py
python data/create_db.py

# 4. Execute o dashboard
streamlit run app.py
```

O dashboard abrirá automaticamente em `http://localhost:8501`.

## 📈 Possíveis evoluções

- Conexão com banco de dados real (PostgreSQL/MySQL)
- Autenticação de usuários
- Exportação de relatórios em PDF/Excel
- Previsão de vendas futuras com Machine Learning

---

Desenvolvido por [Gabriel](https://github.com/gabrielaias) | [LinkedIn](https://www.linkedin.com/in/gabrielaias/)
