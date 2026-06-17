import streamlit as st

from database.projects import (
    listar_projetos,
    criar_projeto
)


def render():

    st.title("📁 Projetos")

    st.subheader("Novo Projeto")

    col1, col2 = st.columns(2)

    with col1:
        codigo = st.text_input("Código")

        nome = st.text_input("Nome do Projeto")

    with col2:
        cliente = st.text_input("Cliente")

        local = st.text_input("Local")

    if st.button(
        "Salvar Projeto",
        use_container_width=True
    ):

        try:

            criar_projeto(
                codigo,
                nome,
                cliente,
                local
            )

            st.success(
                "Projeto cadastrado com sucesso!"
            )

            st.rerun()

        except Exception as e:

            st.error(str(e))

    st.divider()

    st.subheader("Projetos Cadastrados")

    projetos = listar_projetos()

    if projetos:

        dados = []

        for p in projetos:

            dados.append({
                "Código": p.codigo,
                "Projeto": p.nome,
                "Cliente": p.cliente,
                "Local": p.local
            })

        st.dataframe(
            dados,
            use_container_width=True
        )

    else:

        st.info(
            "Nenhum projeto cadastrado."
        )