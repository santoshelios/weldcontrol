import streamlit as st
import pandas as pd
import plotly.express as px

from database.projects import listar_projetos

from database.dashboard_queries import (
    obter_kpis_projeto,
    obter_tipo_junta,
    obter_fluido,
    obter_top_soldadores,
    obter_tabela_analitica
)


def render():

    st.title("📊 Dashboard Executivo")
    st.caption("Controle Gerencial de Soldagem")

    projetos = listar_projetos()

    if not projetos:
        st.warning("Nenhum projeto cadastrado.")
        return

    projeto_dict = {
        p.nome: p.id
        for p in projetos
    }

    # =====================================================
    # FILTROS
    # =====================================================

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:

        projeto = st.selectbox(
            "Projeto",
            list(projeto_dict.keys()),
            key="dashboard_projeto"
        )

    projeto_id = projeto_dict[projeto]

    # filtros preparados para próxima etapa
    with col_f2:
        st.multiselect(
            "Fluido",
            [],
            disabled=True
        )

    with col_f3:
        st.multiselect(
            "Tipo Junta",
            [],
            disabled=True
        )

    with col_f4:
        st.multiselect(
            "Soldador",
            [],
            disabled=True
        )

    kpis = obter_kpis_projeto(
        projeto_id
    )

    # =====================================================
    # CARDS
    # =====================================================

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🔩 Juntas",
            f"{kpis['total']:,}".replace(",", ".")
        )

    with c2:
        st.metric(
            "📈 Avanço",
            f"{kpis['percentual']}%"
        )

    with c3:
        st.metric(
            "🔥 Soldadas",
            f"{kpis['soldadas']:,}".replace(",", ".")
        )

    with c4:
        st.metric(
            "⏳ Pendentes",
            f"{kpis['pendentes']:,}".replace(",", ".")
        )

    # =====================================================
    # FLUIDO
    # =====================================================

    st.divider()

    fluido = obter_fluido(
        projeto_id
    )

    if fluido:

        df_fluido = pd.DataFrame(
            fluido,
            columns=[
                "Fluido",
                "Quantidade"
            ]
        )

        df_fluido = df_fluido.sort_values(
            "Quantidade",
            ascending=False
        )

        fig_fluido = px.bar(
            df_fluido,
            x="Fluido",
            y="Quantidade",
            text="Quantidade",
            title="Mapeamento por Fluido"
        )

        fig_fluido.update_layout(
            height=450,
            showlegend=False
        )

        st.plotly_chart(
            fig_fluido,
            use_container_width=True
        )

    # =====================================================
    # SOLDADORES | TIPO DE JUNTA
    # =====================================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        soldadores = obter_top_soldadores(
            projeto_id
        )

        if soldadores:

            df_soldadores = pd.DataFrame(
                soldadores,
                columns=[
                    "Soldador",
                    "Juntas"
                ]
            )

            df_soldadores = df_soldadores.sort_values(
                "Juntas",
                ascending=False
            )

            fig_soldadores = px.bar(
                df_soldadores,
                x="Soldador",
                y="Juntas",
                text="Juntas",
                title="Top Soldadores"
            )

            fig_soldadores.update_layout(
                height=450
            )

            st.plotly_chart(
                fig_soldadores,
                use_container_width=True
            )

    with col2:

        tipo_junta = obter_tipo_junta(
            projeto_id
        )

        if tipo_junta:

            df_tipo = pd.DataFrame(
                tipo_junta,
                columns=[
                    "Tipo Junta",
                    "Quantidade"
                ]

            )

            df_tipo = df_tipo.sort_values(
                "Quantidade",
                ascending=False
            )

            fig_tipo = px.bar(
                df_tipo,
                x="Quantidade",
                y="Tipo Junta",
                orientation="h",
                text="Quantidade",
                title="Mapeamento por Tipo de Junta"
            )

            fig_tipo.update_layout(
                height=450
            )

            fig_tipo.update_yaxes(
                categoryorder="total ascending"
            )

            st.plotly_chart(
                fig_tipo,
                use_container_width=True
            )

    # =====================================================
    # TABELA ANALÍTICA
    # =====================================================

    st.divider()

    st.subheader("📋 Tabela Analítica")

    tabela = obter_tabela_analitica(
        projeto_id
    )

    if tabela:

        df_tabela = pd.DataFrame(
            tabela
        )

        st.dataframe(
            df_tabela,
            use_container_width=True,
            hide_index=True
        )