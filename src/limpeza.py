import pandas as pd
import re
from loguru import logger


def padronizar_datas(df):
    def converter_data(valor):
        if pd.isna(valor):
            return pd.NaT
        valor = str(valor)
        for formato in ("%d/%m/%Y", "%m-%d-%Y", "%Y-%m-%d"):
            try:
                return pd.to_datetime(valor, format=formato)
            except (ValueError, TypeError):
                continue
        return pd.NaT

    df["data_venda"] = df["data_venda"].apply(converter_data)
    return df


def padronizar_produto(df):
    df["produto"] = df["produto"].astype(str).str.strip().str.title()
    return df


def preencher_categoria(df):
    mapa_categoria = (
        df[df["categoria"].astype(str).str.strip() != ""]
        .groupby("produto")["categoria"]
        .first()
        .to_dict()
    )
    df["categoria"] = df["categoria"].astype(str).str.strip()
    df.loc[df["categoria"] == "", "categoria"] = df.loc[df["categoria"] == "", "produto"].map(mapa_categoria)
    df["categoria"] = df["categoria"].fillna("Nao Informado")
    return df


def remover_qtd_negativa(df):
    antes = len(df)
    df = df[df["quantidade"] > 0].copy()
    removidas = antes - len(df)
    if removidas > 0:
        logger.info(f"Removidas {removidas} linhas com quantidade negativa")
    return df


def padronizar_preco(df):
    def converter_preco(valor):
        if isinstance(valor, str):
            valor = valor.replace(",", ".")
        try:
            return float(valor)
        except (ValueError, TypeError):
            return None

    df["preco_unitario"] = df["preco_unitario"].apply(converter_preco)
    df = df.dropna(subset=["preco_unitario"])
    return df


def recalcular_total(df):
    df["total_venda"] = (df["quantidade"] * df["preco_unitario"]).round(2)
    return df


def padronizar_vendedor(df):
    df["vendedor"] = df["vendedor"].astype(str).str.strip()
    return df


def padronizar_regiao(df):
    mapa_regiao = {
        "sp": "Sudeste",
        "sao paulo": "Sudeste",
        "Sao Paulo": "Sudeste",
        "sul": "Sul",
        "SUL": "Sul",
        "ne": "Nordeste",
        "nordeste": "Nordeste",
        "co": "Centro-Oeste",
        "centro-oeste": "Centro-Oeste",
        "norte": "Norte",
        "NORTE": "Norte",
    }

    def normalizar(valor):
        valor_str = str(valor).strip()
        if valor_str in ("Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"):
            return valor_str
        return mapa_regiao.get(valor_str, mapa_regiao.get(valor_str.lower(), valor_str))

    df["regiao"] = df["regiao"].apply(normalizar)
    return df


def preencher_pagamento(df):
    df["forma_pagamento"] = df["forma_pagamento"].fillna("Nao Informado")
    return df


def validar_dados(df):
    erros = []

    if df["data_venda"].isna().any():
        erros.append(f"{df['data_venda'].isna().sum()} datas invalidas (NaT)")

    if (df["quantidade"] <= 0).any():
        erros.append("Existem quantidades <= 0")

    if df["preco_unitario"].isna().any():
        erros.append("Existem precos nulos")

    if df["categoria"].isna().any() or (df["categoria"] == "").any():
        erros.append("Existem categorias vazias")

    regioes_validas = {"Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"}
    regioes_invalidas = set(df["regiao"].unique()) - regioes_validas
    if regioes_invalidas:
        erros.append(f"Regioes nao padronizadas encontradas: {regioes_invalidas}")

    if erros:
        for erro in erros:
            logger.warning(f"Validacao: {erro}")
    else:
        logger.info("Validacao concluida sem problemas.")

    return df


def limpar_dados(df):
    logger.info(f"Linhas antes da limpeza: {len(df)}")

    df = padronizar_produto(df)
    df = preencher_categoria(df)
    df = padronizar_datas(df)
    df = remover_qtd_negativa(df)
    df = padronizar_preco(df)
    df = recalcular_total(df)
    df = padronizar_vendedor(df)
    df = padronizar_regiao(df)
    df = preencher_pagamento(df)
    df = validar_dados(df)

    logger.info(f"Linhas depois da limpeza: {len(df)}")
    return df


if __name__ == "__main__":
    caminho_entrada = "data/raw/vendas_raw.xlsx"
    caminho_saida = "data/processed/dados_limpos.xlsx"

    df = pd.read_excel(caminho_entrada)
    df_limpo = limpar_dados(df)
    df_limpo.to_excel(caminho_saida, index=False)

    logger.info(f"Arquivo limpo salvo em: {caminho_saida}")