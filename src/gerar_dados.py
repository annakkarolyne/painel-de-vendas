import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')
random.seed(42)

NUM_LINHAS = 500

produtos = {
    "Notebook Dell": "Informatica",
    "Notebook Lenovo": "Informatica",
    "Mouse Logitech": "Informatica",
    "Teclado Mecanico": "Informatica",
    "Monitor LG 24": "Informatica",
    "Smartphone Samsung": "Celulares",
    "Smartphone Motorola": "Celulares",
    "Fone de Ouvido JBL": "Acessorios",
    "Carregador Turbo": "Acessorios",
    "Smart TV 50": "TV e Video",
    "Smart TV 43": "TV e Video",
    "Caixa de Som Bluetooth": "Audio",
    "Console PlayStation 5": "Games",
    "Console Xbox Series S": "Games",
    "Tablet Samsung": "Informatica",
    "Impressora HP": "Informatica",
    "Roteador TP-Link": "Redes",
    "HD Externo 1TB": "Informatica",
    "Pen Drive 64GB": "Acessorios",
    "Webcam Full HD": "Acessorios",
}

regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

formas_pagamento = ["Cartao Credito", "Cartao Debito", "Pix", "Boleto", "Dinheiro"]

vendedores = [fake.name() for _ in range(10)]


def gerar_linha():
    produto = random.choice(list(produtos.keys()))
    categoria = produtos[produto]
    quantidade = random.randint(1, 5)
    preco = round(random.uniform(50, 5000), 2)
    total = round(quantidade * preco, 2)

    if random.random() < 0.15:
        produto_final = random.choice([produto.upper(), produto.lower()])
    else:
        produto_final = produto

    categoria_final = categoria if random.random() > 0.05 else ""

    if random.random() < 0.03:
        quantidade = -quantidade

    if random.random() < 0.2:
        preco_final = str(preco).replace(".", ",")
    else:
        preco_final = preco

    if random.random() < 0.06:
        total_final = round(total * random.choice([0.5, 1.5, 2]), 2)
    else:
        total_final = total

    return produto_final, categoria_final, quantidade, preco_final, total_final


def gerar_data():
    data = fake.date_between(start_date='-1y', end_date='today')
    if random.random() < 0.1:
        return data.strftime("%m-%d-%Y")
    return data.strftime("%d/%m/%Y")


def gerar_vendedor():
    vendedor = random.choice(vendedores)
    if random.random() < 0.1:
        vendedor = "  " + vendedor + "  "
    return vendedor


def gerar_regiao():
    regiao = random.choice(regioes)
    if random.random() < 0.15:
        variacoes = {
            "Sudeste": ["SP", "sao paulo", "Sao Paulo"],
            "Sul": ["sul", "SUL"],
            "Nordeste": ["NE", "nordeste"],
            "Centro-Oeste": ["CO", "centro-oeste"],
            "Norte": ["norte", "NORTE"],
        }
        return random.choice(variacoes.get(regiao, [regiao]))
    return regiao


def gerar_pagamento():
    if random.random() < 0.04:
        return None
    return random.choice(formas_pagamento)


def gerar_dados():
    linhas = []
    for i in range(1, NUM_LINHAS + 1):
        produto, categoria, quantidade, preco, total = gerar_linha()
        linha = {
            "id_venda": 1000 + i,
            "data_venda": gerar_data(),
            "produto": produto,
            "categoria": categoria,
            "quantidade": quantidade,
            "preco_unitario": preco,
            "total_venda": total,
            "vendedor": gerar_vendedor(),
            "regiao": gerar_regiao(),
            "forma_pagamento": gerar_pagamento(),
        }
        linhas.append(linha)
    return pd.DataFrame(linhas)


if __name__ == "__main__":
    df = gerar_dados()
    caminho_saida = "data/raw/vendas_raw.xlsx"
    df.to_excel(caminho_saida, index=False)
    print(f"Arquivo gerado com sucesso: {caminho_saida}")
    print(f"Total de linhas: {len(df)}")