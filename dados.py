from pathlib import Path

import pandas as pd

arquivo = Path(__file__).with_name(
    "Tecnologias e Diretrizes para tratamento e prevenção da Covid-19_Página 1_Tabela.xlsx"
)
df = pd.read_excel(arquivo, na_values=["-"])
df = df.dropna(how="all")

#Tirando colunas com apenas links e ordenção
df = df.drop(columns=["Qtd",
                      "Relatório de Recomendação inicial",
                      "Relatórios para a Sociedade",
                      "Contribuições de experiência e opinião",
                      "Contribuições técnico - científicas",
                      "Relatório de recomendação Final",
                      "Decisão do Ministério da Saúde - Relatório",
                      "Decisão do Ministério da Saúde - Portarias",
                      "Notas Técnicas",
                      "Despacho"])

# Cria a coluna "Data" com a primeira data (dd/mm/aaaa) encontrada em "Demandante"
df["Data"] = pd.to_datetime(
    df["Demandante"].str.extract(r"(\d{2}/\d{2}/\d{4})")[0],
    format="%d/%m/%Y",
    errors="coerce",
)

# Ordena da mais antiga para a mais recente (linhas sem data vão para o fim)
df = df.sort_values("Data", ascending=True, na_position="last").reset_index(drop=True)
df.sort_values(["Data", "Tecnologias e Diretrizes para COVID - 19"])

# Remove a data (e o "em" que vem antes dela) da coluna "Demandante"
df["Demandante"] = (
    df["Demandante"]
    .str.replace(r"\s*em\s+\d{2}/\d{2}/\d{4}", "", regex=True)
    .str.strip()
)

df = df[["Tecnologias e Diretrizes para COVID - 19", "Demandante", "Data", "Análise inicial da Conitec", "Consulta Pública", "Análise Final da Conitec", "Decisão do Ministério da Saúde"]]

saida = Path(__file__).with_name("dados_tratados.xlsx")

with pd.ExcelWriter(saida, engine="openpyxl", date_format="DD/MM/YYYY") as writer:
    df.to_excel(writer, sheet_name="Dados", index=False)