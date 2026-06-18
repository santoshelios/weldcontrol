import streamlit as st
from datetime import date

from database.projects import listar_projetos
from database.isometricos import (
    listar_isometricos,
    salvar_isometrico
)


def render():

    st.title("📐 Planejamento")

    st.caption(
        "Cadastro e controle de isométricos, revisões, spools e juntas planejadas."
    )

    projetos = listar_projetos()

    projeto_dict = {
        p.nome: p.id
        for p in projetos
    }

    st.divider()

    with st.expander("➕ Novo Isométrico", expanded=True):

        with st.form("form_isometrico", clear_on_submit=True):

            st.subheader("📋 Dados Gerais")

            col1, col2, col3 = st.columns(3)

            with col1:

                projeto = st.selectbox(
                    "Projeto",
                    list(projeto_dict.keys()),
                    key="planejamento_projeto"
                )

            with col2:

                desenho = st.text_input(
                    "Desenho Isométrico",
                    placeholder="Ex.: LC-1025-3"
                )

            with col3:

                revisao = st.number_input(
                    "Revisão",
                    min_value=0,
                    value=0,
                    step=1
                )

            st.divider()

            st.subheader("🏗️ Planejamento")

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                sistema = st.text_input(
                    "Sistema"
                )

            with col2:

                area = st.text_input(
                    "Área"
                )

            with col3:

                qtd_spools = st.number_input(
                    "Qtd. Spools",
                    min_value=0,
                    value=0
                )

            with col4:

                qtd_juntas = st.number_input(
                    "Qtd. Juntas",
                    min_value=0,
                    value=0
                )

            st.divider()

            st.subheader("📅 Controle")

            col1, col2 = st.columns(2)

            with col1:

                data_emissao = st.date_input(
                    "Data Emissão",
                    value=date.today()
                )

            with col2:

                status = st.selectbox(
                    "Status",
                    [
                        "Planejado",
                        "Liberado",
                        "Em Produção",
                        "Concluído"
                    ]
                )

            submitted = st.form_submit_button(
                "💾 Salvar Isométrico",
                use_container_width=True
            )

            if submitted:

                if not desenho.strip():

                    st.error(
                        "Informe o desenho."
                    )

                else:

                    salvar_isometrico(
                        projeto_id=projeto_dict[projeto],
                        desenho=desenho.strip().upper(),
                        revisao=revisao,
                        data_emissao=data_emissao,
                        sistema=sistema,
                        area=area,
                        qtd_spools=qtd_spools,
                        qtd_juntas=qtd_juntas,
                        status=status
                    )

                    st.success(
                        "Isométrico cadastrado com sucesso."
                    )

    st.divider()

    st.subheader("📑 Isométricos Cadastrados")

    dados = listar_isometricos()

    if not dados:

        st.info(
            "Nenhum isométrico cadastrado."
        )

    else:

        tabela = []

        for item in dados:

            tabela.append(
                {
                    "ID": item.id,
                    "Desenho": item.desenho,
                    "Rev": item.revisao,
                    "Sistema": item.sistema,
                    "Área": item.area,
                    "Spools": item.qtd_spools,
                    "Juntas": item.qtd_juntas,
                    "Status": item.status,
                    "Ativo": item.ativo
                }
            )

        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True
        )