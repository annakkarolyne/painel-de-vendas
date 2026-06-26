# Decisões Técnicas — Painel de Vendas

## Por que PostgreSQL em vez de MySQL?
PostgreSQL tem suporte nativo a tipos de dados mais ricos, melhor conformidade com SQL padrão e integração mais madura com SQLAlchemy e Power BI.

## Por que Docker para o banco?
Evita conflitos com instalações locais, garante reprodutibilidade e facilita o reset do ambiente durante o desenvolvimento.

## Por que Faker para gerar os dados?
Permite criar dados realistas com erros propositais de forma controlada, simulando um cenário real de limpeza de dados.

## Por que modelo estrela?
É o modelo mais adequado para dashboards analíticos — consultas mais rápidas e estrutura mais simples para o Power BI criar relacionamentos.

## Por que loguru em vez de print?
Loguru fornece logs formatados com nível, timestamp e contexto, facilitando o debug do pipeline em produção.
