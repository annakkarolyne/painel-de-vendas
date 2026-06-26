import pandas as pd
from sqlalchemy import create_engine
from loguru import logger


def get_engine():
    url = "postgresql+psycopg://ana:painel1234@127.0.0.1:5432/painel_vendas"
    return create_engine(url)


def carregar_dados(df, engine):
    with engine.begin() as conn:
        produtos = df[["produto", "categoria"]].drop_duplicates().reset_index(drop=True)
        produtos.columns = ["nome_produto", "categoria"]
        produtos.to_sql("dim_produto", conn, if_exists="append", index=False)
        logger.info(f"dim_produto: {len(produtos)} registros inseridos")

        vendedores = df[["vendedor"]].drop_duplicates().reset_index(drop=True)
        vendedores.columns = ["nome_vendedor"]
        vendedores.to_sql("dim_vendedor", conn, if_exists="append", index=False)
        logger.info(f"dim_vendedor: {len(vendedores)} registros inseridos")

        regioes = df[["regiao"]].drop_duplicates().reset_index(drop=True)
        regioes.to_sql("dim_regiao", conn, if_exists="append", index=False)
        logger.info(f"dim_regiao: {len(regioes)} registros inseridos")

        pagamentos = df[["forma_pagamento"]].drop_duplicates().reset_index(drop=True)
        pagamentos.to_sql("dim_pagamento", conn, if_exists="append", index=False)
        logger.info(f"dim_pagamento: {len(pagamentos)} registros inseridos")

        dim_prod = pd.read_sql("SELECT id_produto, nome_produto FROM dim_produto", conn)
        dim_vend = pd.read_sql("SELECT id_vendedor, nome_vendedor FROM dim_vendedor", conn)
        dim_reg = pd.read_sql("SELECT id_regiao, regiao FROM dim_regiao", conn)
        dim_pag = pd.read_sql("SELECT id_pagamento, forma_pagamento FROM dim_pagamento", conn)

        fato = df.merge(dim_prod, left_on="produto", right_on="nome_produto")
        fato = fato.merge(dim_vend, left_on="vendedor", right_on="nome_vendedor")
        fato = fato.merge(dim_reg, on="regiao")
        fato = fato.merge(dim_pag, on="forma_pagamento")

        fato_final = fato[["id_venda", "data_venda", "quantidade", "preco_unitario", "total_venda", "id_produto", "id_vendedor", "id_regiao", "id_pagamento"]].drop_duplicates(subset=["id_venda"])
        fato_final.to_sql("fato_vendas", conn, if_exists="append", index=False)
        logger.info(f"fato_vendas: {len(fato_final)} registros inseridos")


if __name__ == "__main__":
    engine = get_engine()
    df = pd.read_excel("data/processed/dados_limpos.xlsx")
    carregar_dados(df, engine)
    logger.info("Carga concluida com sucesso!")