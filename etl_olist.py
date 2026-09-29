import pandas as pd
from pathlib import Path


# ============================================================
# ETL - DESEMPENHO DAS VENDAS NO E-COMMERCE BRASILEIRO
# Dataset: Brazilian E-Commerce Public Dataset by Olist
# ============================================================


# Caminhos das pastas
PASTA_RAW = Path("dados/raw")
PASTA_PROCESSED = Path("dados/processed")


# ============================================================
# 1. EXTRAÇÃO
# ============================================================

print("=" * 60)
print("ETAPA 1 - EXTRAÇÃO DOS DADOS")
print("=" * 60)


orders = pd.read_csv(
    PASTA_RAW / "olist_orders_dataset.csv"
)

order_items = pd.read_csv(
    PASTA_RAW / "olist_order_items_dataset.csv"
)

products = pd.read_csv(
    PASTA_RAW / "olist_products_dataset.csv"
)

customers = pd.read_csv(
    PASTA_RAW / "olist_customers_dataset.csv"
)

sellers = pd.read_csv(
    PASTA_RAW / "olist_sellers_dataset.csv"
)


print(f"Orders:       {len(orders)} registros")
print(f"Order Items:  {len(order_items)} registros")
print(f"Products:     {len(products)} registros")
print(f"Customers:    {len(customers)} registros")
print(f"Sellers:      {len(sellers)} registros")

print("\nExtração concluída!")

# ============================================================
# 2. TRATAMENTO - DIAGNÓSTICO DOS DADOS
# ============================================================

print("\n" + "=" * 60)
print("ETAPA 2 - DIAGNÓSTICO DOS DADOS")
print("=" * 60)


# Verificação de valores nulos
print("\n--- VALORES NULOS ---")

print("\nOrders:")
print(orders.isnull().sum())

print("\nOrder Items:")
print(order_items.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nCustomers:")
print(customers.isnull().sum())

print("\nSellers:")
print(sellers.isnull().sum())


# Verificação de duplicidades
print("\n--- DUPLICIDADES ---")

print(f"Orders duplicados: {orders.duplicated().sum()}")
print(f"Order Items duplicados: {order_items.duplicated().sum()}")
print(f"Products duplicados: {products.duplicated().sum()}")
print(f"Customers duplicados: {customers.duplicated().sum()}")
print(f"Sellers duplicados: {sellers.duplicated().sum()}")

# ============================================================
# 3. TRATAMENTO DOS DADOS
# ============================================================

print("\n" + "=" * 60)
print("ETAPA 3 - TRATAMENTO DOS DADOS")
print("=" * 60)


# ------------------------------------------------------------
# Conversão das datas da tabela Orders
# ------------------------------------------------------------

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

orders["order_approved_at"] = pd.to_datetime(
    orders["order_approved_at"]
)

orders["order_delivered_carrier_date"] = pd.to_datetime(
    orders["order_delivered_carrier_date"]
)

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"]
)

orders["order_estimated_delivery_date"] = pd.to_datetime(
    orders["order_estimated_delivery_date"]
)


# ------------------------------------------------------------
# Tratamento das categorias dos produtos
# ------------------------------------------------------------

products["product_category_name"] = products[
    "product_category_name"
].fillna("Não informado")


# ------------------------------------------------------------
# Garantia dos tipos numéricos
# ------------------------------------------------------------

order_items["price"] = pd.to_numeric(
    order_items["price"],
    errors="coerce"
)

order_items["freight_value"] = pd.to_numeric(
    order_items["freight_value"],
    errors="coerce"
)


print("Tratamento concluído!")

# ============================================================
# 4.1 - CRIAÇÃO DA DIMENSÃO CLIENTE
# ============================================================

print("\n" + "=" * 60)
print("4.1 - CRIANDO D_CLIENTE")
print("=" * 60)


D_Cliente = customers[
    [
        "customer_id",
        "customer_unique_id",
        "customer_city",
        "customer_state"
    ]
].copy()


# Criação da chave substituta
D_Cliente.insert(
    0,
    "cliente_sk",
    range(1, len(D_Cliente) + 1)
)


print(f"D_Cliente criada: {len(D_Cliente)} registros")
print(D_Cliente.head())

# ============================================================
# 4.2 - CRIAÇÃO DA DIMENSÃO PRODUTO
# ============================================================

print("\n" + "=" * 60)
print("4.2 - CRIANDO D_PRODUTO")
print("=" * 60)


D_Produto = products[
    [
        "product_id",
        "product_category_name"
    ]
].copy()


# Criação da chave substituta
D_Produto.insert(
    0,
    "produto_sk",
    range(1, len(D_Produto) + 1)
)


print(f"D_Produto criada: {len(D_Produto)} registros")
print(D_Produto.head())

# ============================================================
# 4.3 - CRIAÇÃO DA DIMENSÃO VENDEDOR
# ============================================================

print("\n" + "=" * 60)
print("4.3 - CRIANDO D_VENDEDOR")
print("=" * 60)


D_Vendedor = sellers[
    [
        "seller_id",
        "seller_city",
        "seller_state"
    ]
].copy()


# Criação da chave substituta
D_Vendedor.insert(
    0,
    "vendedor_sk",
    range(1, len(D_Vendedor) + 1)
)


print(f"D_Vendedor criada: {len(D_Vendedor)} registros")
print(D_Vendedor.head())

# ============================================================
# 4.4 - CRIAÇÃO DA DIMENSÃO TEMPO
# ============================================================

print("\n" + "=" * 60)
print("4.4 - CRIANDO D_TEMPO")
print("=" * 60)


# Obtém as datas únicas de compra
D_Tempo = pd.DataFrame({
    "data": orders["order_purchase_timestamp"].dt.normalize().unique()
})


# Ordena as datas
D_Tempo = D_Tempo.sort_values("data").reset_index(drop=True)


# Criação da chave substituta
D_Tempo.insert(
    0,
    "tempo_sk",
    range(1, len(D_Tempo) + 1)
)


# Criação dos atributos de calendário
D_Tempo["ano"] = D_Tempo["data"].dt.year
D_Tempo["mes"] = D_Tempo["data"].dt.month

D_Tempo["nome_mes"] = D_Tempo["data"].dt.month_name(
    locale="pt_BR"
)

D_Tempo["trimestre"] = D_Tempo["data"].dt.quarter

D_Tempo["dia"] = D_Tempo["data"].dt.day

D_Tempo["dia_semana"] = D_Tempo["data"].dt.day_name(
    locale="pt_BR"
)


print(f"D_Tempo criada: {len(D_Tempo)} registros")
print(D_Tempo.head())

# ============================================================
# 4.5 - CRIAÇÃO DA TABELA F_VENDAS
# ============================================================

print("\n" + "=" * 60)
print("4.5 - CRIANDO F_VENDAS")
print("=" * 60)


# ------------------------------------------------------------
# Junta os itens dos pedidos com os dados dos pedidos
# ------------------------------------------------------------

F_Vendas = order_items.merge(
    orders[
        [
            "order_id",
            "customer_id",
            "order_purchase_timestamp"
        ]
    ],
    on="order_id",
    how="left"
)


print(f"Registros após junção com orders: {len(F_Vendas)}")

# ------------------------------------------------------------
# Associação com D_Cliente
# ------------------------------------------------------------

F_Vendas = F_Vendas.merge(
    D_Cliente[
        [
            "cliente_sk",
            "customer_id"
        ]
    ],
    on="customer_id",
    how="left"
)

# ------------------------------------------------------------
# Associação com D_Produto
# ------------------------------------------------------------

F_Vendas = F_Vendas.merge(
    D_Produto[
        [
            "produto_sk",
            "product_id"
        ]
    ],
    on="product_id",
    how="left"
)

# ------------------------------------------------------------
# Associação com D_Vendedor
# ------------------------------------------------------------

F_Vendas = F_Vendas.merge(
    D_Vendedor[
        [
            "vendedor_sk",
            "seller_id"
        ]
    ],
    on="seller_id",
    how="left"
)

# ------------------------------------------------------------
# Associação com D_Tempo
# ------------------------------------------------------------

F_Vendas["data"] = (
    F_Vendas["order_purchase_timestamp"].dt.normalize()
)

F_Vendas = F_Vendas.merge(
    D_Tempo[
        [
            "tempo_sk",
            "data"
        ]
    ],
    on="data",
    how="left"
)

# ------------------------------------------------------------
# Seleção dos campos finais
# ------------------------------------------------------------

F_Vendas = F_Vendas[
    [
        "order_id",
        "order_item_id",
        "cliente_sk",
        "produto_sk",
        "vendedor_sk",
        "tempo_sk",
        "price",
        "freight_value"
    ]
].copy()

# ------------------------------------------------------------
# Criação da chave substituta da venda
# ------------------------------------------------------------

F_Vendas.insert(
    0,
    "venda_sk",
    range(1, len(F_Vendas) + 1)
)

# ============================================================
# VALIDAÇÃO DA F_VENDAS
# ============================================================

print("\n--- VALIDAÇÃO DA F_VENDAS ---")

print(f"Total de registros: {len(F_Vendas)}")

print(f"Valores nulos:")
print(F_Vendas.isnull().sum())

print(f"\nDuplicidades completas: {F_Vendas.duplicated().sum()}")

print("\nPrimeiros registros:")
print(F_Vendas.head())

# ============================================================
# 5 - CARGA DOS DADOS TRANSFORMADOS
# ============================================================

print("\n" + "=" * 60)
print("ETAPA 5 - CARGA DOS DADOS")
print("=" * 60)


# Cria a pasta de saída caso ela ainda não exista
PASTA_PROCESSED.mkdir(parents=True, exist_ok=True)


# Salva as dimensões
D_Cliente.to_csv(
    PASTA_PROCESSED / "D_Cliente.csv",
    index=False,
    encoding="utf-8-sig"
)

D_Produto.to_csv(
    PASTA_PROCESSED / "D_Produto.csv",
    index=False,
    encoding="utf-8-sig"
)

D_Vendedor.to_csv(
    PASTA_PROCESSED / "D_Vendedor.csv",
    index=False,
    encoding="utf-8-sig"
)

D_Tempo.to_csv(
    PASTA_PROCESSED / "D_Tempo.csv",
    index=False,
    encoding="utf-8-sig"
)


# Salva a tabela fato
F_Vendas.to_csv(
    PASTA_PROCESSED / "F_Vendas.csv",
    index=False,
    encoding="utf-8-sig"
)


print("D_Cliente.csv salvo!")
print("D_Produto.csv salvo!")
print("D_Vendedor.csv salvo!")
print("D_Tempo.csv salvo!")
print("F_Vendas.csv salvo!")

print("\nCarga concluída com sucesso!")

# ============================================================
# 6 - VALIDAÇÃO FINAL DO ETL
# ============================================================

print("\n" + "=" * 60)
print("ETAPA 6 - VALIDAÇÃO FINAL")
print("=" * 60)


# Validação das chaves primárias das dimensões
print("\n--- CHAVES PRIMÁRIAS ---")

print(
    "D_Cliente:",
    D_Cliente["cliente_sk"].is_unique
)

print(
    "D_Produto:",
    D_Produto["produto_sk"].is_unique
)

print(
    "D_Vendedor:",
    D_Vendedor["vendedor_sk"].is_unique
)

print(
    "D_Tempo:",
    D_Tempo["tempo_sk"].is_unique
)

print(
    "F_Vendas:",
    F_Vendas["venda_sk"].is_unique
)


# Validação das chaves estrangeiras
print("\n--- CHAVES ESTRANGEIRAS ---")

clientes_invalidos = ~F_Vendas["cliente_sk"].isin(
    D_Cliente["cliente_sk"]
)

produtos_invalidos = ~F_Vendas["produto_sk"].isin(
    D_Produto["produto_sk"]
)

vendedores_invalidos = ~F_Vendas["vendedor_sk"].isin(
    D_Vendedor["vendedor_sk"]
)

tempos_invalidos = ~F_Vendas["tempo_sk"].isin(
    D_Tempo["tempo_sk"]
)


print(
    "Clientes sem correspondência:",
    clientes_invalidos.sum()
)

print(
    "Produtos sem correspondência:",
    produtos_invalidos.sum()
)

print(
    "Vendedores sem correspondência:",
    vendedores_invalidos.sum()
)

print(
    "Datas sem correspondência:",
    tempos_invalidos.sum()
)


# Resumo final
print("\n--- RESUMO FINAL ---")

print(f"D_Cliente:   {len(D_Cliente)} registros")
print(f"D_Produto:   {len(D_Produto)} registros")
print(f"D_Vendedor:  {len(D_Vendedor)} registros")
print(f"D_Tempo:     {len(D_Tempo)} registros")
print(f"F_Vendas:    {len(F_Vendas)} registros")

print("\nETL CONCLUÍDO E VALIDADO COM SUCESSO!")
