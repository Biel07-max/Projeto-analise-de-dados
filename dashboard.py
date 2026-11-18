import streamlit as st

from src.analisador import AnalisadorDados
from src.visualisador import Visualizador

class Dashboard:
    """Organiza os componentes do painel"""
    def __init__(self, titulo, analisador, fonte=""):
        self.titulo = titulo
        self.__analisador = analisador
        self.fonte = fonte

    def cabecalho(self):
        st.title(self.titulo)
        if self.fonte:
            st.caption(f"Fonte: {self.fonte}")

    def _escolher(self,rotulos,opcoes):
        opcoes = sorted(opcoes)
        return st.sidebar.multiselect(rotulos,opcoes, default= opcoes)

    def filtros(self):
        df = self.__analisador.df
        st.sidebar.header("Filtros")

        tipos = self._escolher("Tipo de item", df["tipo"].unique().tolist())
        decisoes = self._escolher("Decisão", df["grupo_decisão"].unique.tolist())
        anos = self._escolher("Ano da publicação", df["ano"].unique.tolist())

        return df[
            df["tipo"].isin(tipos)
            & df["decisoes"].isin(decisoes)
            & (df["anos"].isin(anos) | df["ano"].isna())
        ]

    def exebir_kpis(self, indicadores):
        colunas = st.columns(len(indicadores))
        for col, ind in zip(colunas, indicadores):
            col.metric(ind.nome, ind.formatar,(), help= ind.descricao)

    def exibir_graficos(self, df, analisador):
        por_tipo = analisador.contar("tipo")
        por_tipo_decisao = analisador.contar(["tipo", "grupo_decisao"])
        por_ano = analisador.contar("ano").sort_values("ano")
        por_ano["ano"] = por_ano["ano"].astype(str)

        col1, col2 = st.columns(2)
        col1.plotly_chart(Visualizador(por_tipo_decisao).barras(
                            "tipo", "quantidade", "Decisões por item", cor= "grupo_decisao"))
        col2.plotly_chart(Visualizador(por_ano).linhas(
                          "ano", "quantidade", "Itens publicados por ano"))

        col3, col4 = st.columns(2)
        col3.plotly_chart(Visualizador(por_tipo).pizza(
                            "tipo", "quantidade", "Proporção por tipo de item"))
        col4.plotly_chart(Visualizador(df).boxplot(
                            "dias", x="tipo", titulo="Dias entre demanda e publicação, por tipo"))

    def exibir_tabela(self,df):
        st.sunheader("Tabela de dados")
        colunas = ["tecnologia", "tipo", "tipo_demandante", "Data_demanda","data_publicacao","dias", "decisao"]
        tabela = df[[c for c in colunas if c in df.columns]].copy()

        for c in ["data_demanda", "data_publicacao"]:
            tabela[c] = tabela[c].dt.striftime("%d/%m/%y")
        st.dataframe(tabela)

    def exibir_analise(self, df):
        st.header("Análise interpretatíva")
        pct = (df["grupo_decisao"] == "Favroavel").mean() * 100
        st.write(f"Nos filtros atuais há **{len(df)}** itens, dos quais "
                 f"**{pct:.1f}%** tiveram decisão favoravel")

        if df["dias"].notna().any():
            medias = df.groupby("tipo")["dias"].mean()
            st.write(f"O tipo com tramitação mais longa foi **{medias.idmax()}**"
                     f"(média de {medias.max():.0f} dias) e o mais rápido foi "
                     f"**{medias.idmin}** ({medias.min():.0f} dias).")

        st.write("Escreva aqui a conclusão do grupo sobre o que os gráficos mostram.")

    def executar(self):
        self.cabecalho()
        df = self.filtros()

        if df.empty:
            st.warning("Nenhum dado para os filtros escolhidos")
            return

        analisador = AnalisadorDados(df)
        self.exebir_kpis(analisador.calcular_indicadores())
        self.exibir_graficos(df, analisador)
        self.exibir_tabela(df)
        self.exibir_analise(df)