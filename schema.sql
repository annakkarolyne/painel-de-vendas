-- Dimensões
CREATE TABLE dim_produto (
    id_produto SERIAL PRIMARY KEY,
    nome_produto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL
);

CREATE TABLE dim_vendedor (
    id_vendedor SERIAL PRIMARY KEY,
    nome_vendedor VARCHAR(100) NOT NULL
);

CREATE TABLE dim_regiao (
    id_regiao SERIAL PRIMARY KEY,
    regiao VARCHAR(50) NOT NULL
);

CREATE TABLE dim_pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    forma_pagamento VARCHAR(50) NOT NULL
);

-- Fato
CREATE TABLE fato_vendas (
    id_venda INTEGER PRIMARY KEY,
    data_venda DATE NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario NUMERIC(10,2) NOT NULL,
    total_venda NUMERIC(10,2) NOT NULL,
    id_produto INTEGER REFERENCES dim_produto(id_produto),
    id_vendedor INTEGER REFERENCES dim_vendedor(id_vendedor),
    id_regiao INTEGER REFERENCES dim_regiao(id_regiao),
    id_pagamento INTEGER REFERENCES dim_pagamento(id_pagamento)
);

-- Índices
CREATE INDEX idx_fato_data ON fato_vendas(data_venda);
CREATE INDEX idx_fato_produto ON fato_vendas(id_produto);

-- View
CREATE VIEW vendas_consolidadas AS
SELECT
    f.id_venda,
    f.data_venda,
    p.nome_produto,
    p.categoria,
    f.quantidade,
    f.preco_unitario,
    f.total_venda,
    v.nome_vendedor,
    r.regiao,
    pg.forma_pagamento
FROM fato_vendas f
JOIN dim_produto p ON f.id_produto = p.id_produto
JOIN dim_vendedor v ON f.id_vendedor = v.id_vendedor
JOIN dim_regiao r ON f.id_regiao = r.id_regiao
JOIN dim_pagamento pg ON f.id_pagamento = pg.id_pagamento;