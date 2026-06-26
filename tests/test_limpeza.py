import pytest
import pandas as pd
from src.limpeza import (
    padronizar_datas,
    padronizar_produto,
    remover_qtd_negativa,
    padronizar_preco,
    recalcular_total,
    padronizar_regiao,
    preencher_pagamento,
)


def test_padronizar_datas():
    df = pd.DataFrame({"data_venda": ["15/06/2024", "06-15-2024", "2024-06-15"]})
    df = padronizar_datas(df)
    assert df["data_venda"].isna().sum() == 0
    assert pd.api.types.is_datetime64_any_dtype(df["data_venda"])


def test_remover_qtd_negativa():
    df = pd.DataFrame({"quantidade": [1, -2, 3, -1, 5]})
    df = remover_qtd_negativa(df)
    assert (df["quantidade"] > 0).all()
    assert len(df) == 3


def test_padronizar_preco():
    df = pd.DataFrame({"preco_unitario": ["1.500,99", "299.99", 100]})
    df = padronizar_preco(df)
    assert df["preco_unitario"].isna().sum() == 0
    assert pd.api.types.is_float_dtype(df["preco_unitario"])


def test_recalcular_total():
    df = pd.DataFrame({
        "quantidade": [2, 3],
        "preco_unitario": [100.0, 50.0],
        "total_venda": [999.0, 999.0],  # valores errados propositais
    })
    df = recalcular_total(df)
    assert df["total_venda"].tolist() == [200.0, 150.0]


def test_padronizar_regiao():
    df = pd.DataFrame({"regiao": ["SP", "sul", "NE", "Norte", "CO"]})
    df = padronizar_regiao(df)
    regioes_validas = {"Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste"}
    assert set(df["regiao"].unique()).issubset(regioes_validas)


def test_preencher_pagamento():
    df = pd.DataFrame({"forma_pagamento": [None, "Pix", None]})
    df = preencher_pagamento(df)
    assert df["forma_pagamento"].isna().sum() == 0
    assert "Nao Informado" in df["forma_pagamento"].values