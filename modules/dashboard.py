import streamlit as st
import pandas as pd
import plotly.express as px


st.markdown("""
<style>

div[data-testid="stMetric"]{
    background:#0f172a;
    padding:15px;
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)
from io import BytesIO
from database.projects import listar_projetos

from database.dashboard_queries import (
    obter_kpis_projeto,
    obter_tipo_junta,
    obter_fluido,
    obter_top_soldadores,
    obter_tabela_analitica,
    listar_fluidos,
    listar_tipos_junta
)


st.markdown("""
<style>

div[data-testid="metric-container"]{
    background: linear-gradient(135deg,#0f172a,#1e293b);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:14px;
    padding:12px;
    box-shadow:0 4px 12px rgba(0,0,0,0.15);
}

div[data-testid="metric-container"] label{
    color:#cbd5e1 !important;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)


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

    with col_f2:

        filtro_fluido = st.multiselect(
        "Fluido",
        options=listar_fluidos(projeto_id)
    )

    with col_f3:

        filtro_tipo = st.multiselect(
        "Tipo Junta",
        options=listar_tipos_junta(projeto_id)
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
    # CARDS PRINCIPAIS
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
            "🔥 Soldadas",
            f"{kpis['soldadas']:,}".replace(",", ".")
        )

    with c3:
        st.metric(
            "⏳ Pendentes",
            f"{kpis['pendentes']:,}".replace(",", ".")
        )

    with c4:
        st.metric(
            "📈 Avanço",
            f"{kpis['percentual']}%"
        )

    # =====================================================
    # ENSAIOS
    # =====================================================

    e1, e2, e3, e4, e5, e6 = st.columns(6)

    with e1:
        st.metric(
            "🧪 EVS Real",
            f"{kpis['evs_real']:,}".replace(",", ".")
        )

    with e2:
        st.metric(
            "📋 EVS Pend",
            f"{kpis['evs_pend']:,}".replace(",", ".")
        )

    with e3:
        st.metric(
            "🔬 LP Real",
            f"{kpis['lp_real']:,}".replace(",", ".")
        )

    with e4:
        st.metric(
            "📋 LP Pend",
            f"{kpis['lp_pend']:,}".replace(",", ".")
        )

    with e5:
        st.metric(
            "📡 US Real",
            f"{kpis['us_real']:,}".replace(",", ".")
        )

    with e6:
        st.metric(
            "📋 US Pend",
            f"{kpis['us_pend']:,}".replace(",", ".")
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

    tabela = obter_tabela_analitica(
        projeto_id
    )

    if tabela:

        df_tabela = pd.DataFrame(
            tabela
        )

        df_tabela = df_tabela[
            df_tabela["Fluido"].notna()
        ]

        df_tabela = df_tabela[
            df_tabela["Fluido"].astype(str).str.strip() != ""
        ]

        df_tabela = df_tabela.rename(
        columns={
        "Fluido": "Fluido",
        "Qtde_Juntas": "Qtde Juntas",

        "EVS_Real": "EVS Real",
        "EVS_Pend": "EVS Pend",

        "LP_Real": "LP Real",
        "LP_Pend": "LP Pend",

        "US_Real": "US Real",
        "US_Pend": "US Pend",

        "Soldadas": "Soldadas",
        "Pendentes": "Pendentes",
        "Avanço_%": "Avanço %"
    }
)

        df_tabela = df_tabela[
    [
        "Fluido",
        "Qtde Juntas",

        "EVS Real",
        "EVS Pend",

        "LP Real",
        "LP Pend",

        "US Real",
        "US Pend",

        "Avanço %",
        "Soldadas",
        "Pendentes"
    ]
]

        df_tabela = df_tabela.sort_values(
            by="Qtde Juntas",
            ascending=False
        )

        df_tabela["Avanço %"] = (
            df_tabela["Avanço %"]
            .astype(float)
            .round(1)
            .astype(str)
            + "%"
        )

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            df_tabela.to_excel(
                writer,
                index=False,
                sheet_name="Analise"
            )

        col_titulo, col_espaco, col_botao = st.columns([8, 3, 1])

        with col_titulo:
            st.subheader("📋 Tabela Analítica")

        with col_botao:
            st.download_button(
        label="📥 Exportar",
        data=output.getvalue(),
        file_name="Analise_WeldControl.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

        st.dataframe(
            df_tabela,
            use_container_width=True,
            hide_index=True
        )

        total_juntas = pd.to_numeric(
            df_tabela["Qtde Juntas"]
        ).sum()

        total_soldadas = pd.to_numeric(
            df_tabela["Soldadas"]
        ).sum()

        total_pendentes = pd.to_numeric(
            df_tabela["Pendentes"]
        ).sum()

        st.caption(
            f"""
📌 Total de Juntas: {total_juntas:,}
 | Soldadas: {total_soldadas:,}
 | Pendentes: {total_pendentes:,}
""".replace(",", ".")
        )