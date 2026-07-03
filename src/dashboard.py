import pandas as pd
import matplotlib.pyplot as plt

# ============================
# Leitura do arquivo
# ============================

arquivo = "dados/relatorio (3).csv"

df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin1",
    engine="python",
    on_bad_lines="skip"
)

# ============================
# Limpeza das colunas
# ============================

df.columns = (
    df.columns
    .str.replace("Ã©", "é", regex=False)
    .str.replace("Ã£", "ã", regex=False)
    .str.replace("Ã§", "ç", regex=False)
    .str.replace("Ãµ", "õ", regex=False)
    .str.replace("Ã­", "í", regex=False)
    .str.replace("Ã³", "ó", regex=False)
    .str.replace("Ãº", "ú", regex=False)
    .str.strip()
)

# ============================
# Conversões
# ============================

df["Valor"] = (
    df["Valor"]
    .fillna("0")
    .astype(str)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)

df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

df["Data de emissão"] = pd.to_datetime(
    df["Data de emissão"],
    dayfirst=True,
    errors="coerce"
)

# ============================
# KPIs
# ============================

print("=" * 60)
print("DASHBOARD DE COMPRAS")
print("=" * 60)

print(f"Total de compras: {len(df)}")
print(f"Valor total comprado: R$ {df['Valor'].sum():,.2f}")
print(f"Ticket médio: R$ {df['Valor'].mean():,.2f}")
print(f"Fornecedores únicos: {df['Fornecedor'].nunique()}")
print(f"Operadores: {df['Operador'].nunique()}")

print("=" * 60)

# ============================
# Gráfico 1
# Valor por mês
# ============================

compras_mes = (
    df.groupby(df["Data de emissão"].dt.month)["Valor"]
    .sum()
)

plt.figure(figsize=(10,5))
compras_mes.plot(kind="bar")

plt.title("Valor Comprado por Mês")
plt.xlabel("Mês")
plt.ylabel("Valor (R$)")

plt.tight_layout()
plt.savefig("graficos/valor_por_mes.png")
plt.show()

# ============================
# Gráfico 2
# Top fornecedores
# ============================

top_fornecedores = (
    df.groupby("Fornecedor")["Valor"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,5))
top_fornecedores.plot(kind="bar")

plt.title("Top 10 Fornecedores")
plt.xlabel("Fornecedor")
plt.ylabel("Valor (R$)")

plt.tight_layout()
plt.savefig("graficos/top_fornecedores.png")
plt.show()

# ============================
# Gráfico 3
# Status
# ============================

status = df["Status"].value_counts()

plt.figure(figsize=(8,5))
status.plot(kind="bar")

plt.title("Compras por Status")
plt.xlabel("Status")
plt.ylabel("Quantidade")

plt.tight_layout()
plt.savefig("graficos/status_compras.png")
plt.show()

# ============================
# Gráfico 4
# Operadores
# ============================

operadores = df["Operador"].value_counts()

plt.figure(figsize=(10,5))
operadores.plot(kind="bar")

plt.title("Compras por Operador")
plt.xlabel("Operador")
plt.ylabel("Quantidade")

plt.tight_layout()
plt.savefig("graficos/compras_operador.png")
plt.show()

# ============================
# Gráfico 5
# Condição de pagamento
# ============================

pagamento = df["Condições de pagamento"].value_counts()

plt.figure(figsize=(10,5))
pagamento.plot(kind="bar")

plt.title("Condições de Pagamento")
plt.xlabel("Condição")
plt.ylabel("Quantidade")

plt.tight_layout()
plt.savefig("graficos/condicoes_pagamento.png")
plt.show()
# ============================
# Gráfico 6
# Curva ABC dos fornecedores
# ============================

abc = (
    df.groupby("Fornecedor")["Valor"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

abc["Percentual"] = abc["Valor"] / abc["Valor"].sum() * 100
abc["Percentual acumulado"] = abc["Percentual"].cumsum()

plt.figure(figsize=(12, 6))

plt.bar(abc["Fornecedor"].head(10), abc["Valor"].head(10))
plt.plot(
    abc["Fornecedor"].head(10),
    abc["Percentual acumulado"].head(10),
    marker="o"
)

plt.title("Curva ABC de Fornecedores")
plt.xlabel("Fornecedor")
plt.ylabel("Valor / Percentual acumulado")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig("graficos/curva_abc_fornecedores.png")
plt.show()

print("\nTop 10 fornecedores por valor:")
print(abc.head(10))