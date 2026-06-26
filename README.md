# 📊 Painel de Vendas — Loja de Eletrônicos

Dashboard de vendas completo construído com Python, PostgreSQL e Power BI, simulando um ambiente real de análise de dados em uma loja de eletrônicos.

---

## 🖥️ Demo

> Print ou GIF do dashboard aqui

---

## 🏗️ Arquitetura

\\\
Excel (dados brutos)
    ↓
Python (limpeza e geração)
    ↓
PostgreSQL (modelo estrela via Docker)
    ↓
Power BI (dashboard interativo)
\\\

---

## 🚀 Como rodar o projeto

### Pré-requisitos
- Python 3.11+
- Docker Desktop
- Power BI Desktop

### Passo a passo

\\\ash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/painel-vendas.git
cd painel-vendas

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Suba o banco de dados
docker-compose up -d

# 5. Execute o pipeline completo
python src/pipeline.py
\\\

---

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-compose-blue)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)
![pandas](https://img.shields.io/badge/pandas-2.0-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)

---

## 📁 Estrutura do projeto

\\\
painel-vendas/
├── data/
│   ├── raw/            # Dados brutos gerados
│   └── processed/      # Dados limpos
├── src/
│   ├── gerar_dados.py  # Geração de dados com Faker
│   ├── limpeza.py      # Limpeza e validação
│   ├── carga_db.py     # Carga no PostgreSQL
│   └── pipeline.py     # Orquestrador
├── tests/
│   └── test_limpeza.py # Testes pytest
├── docker-compose.yml
├── schema.sql
├── requirements.txt
└── README.md
\\\

---

## 📈 Aprendizados

- Modelagem dimensional (modelo estrela) com fato e dimensões
- Pipeline ETL completo: geração → limpeza → carga → visualização
- Uso de Docker para isolar o banco de dados
- Criação de medidas DAX no Power BI
- Boas práticas: testes automatizados, logging com loguru, variáveis de ambiente com dotenv
