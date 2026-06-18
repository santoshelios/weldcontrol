import streamlit as st
import pandas as pd

from database.projects import listar_projetos

from database.juntas import (
    excluir_juntas_projeto,
    importar_dataframe_juntas,
    contar_juntas_projeto
)


def render():

    st.title("📤 Upload Weld List")

    st.caption(
        "Importação da Weld List para atualização da produção."
    )

    projetos = listar_projetos()

    projeto_dict = {
        p.nome: p.id
        for p in projetos
    }

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        projeto = st.selectbox(
        "Projeto",
        list(projeto_dict.keys()),
        key="upload_projeto"
)

    with col2:

        arquivo = st.file_uploader(
            "Selecionar Weld List",
            type=["xlsx", "xls"]
        )

    st.divider()

    if arquivo is not None:

        try:

            df = pd.read_excel(arquivo)
            if df.empty:
                st.error("O arquivo está vazio.")
                return

            total_juntas = len(df)

            total_isometricos = (
                df["DESENHO DE MONTAGEM"].nunique()
                if "DESENHO DE MONTAGEM" in df.columns
                else 0
            )

            total_soldadores = (
                df["SOLDADOR RAIZ"].nunique()
                if "SOLDADOR RAIZ" in df.columns
                else 0
            )

            st.success(
                "Arquivo carregado com sucesso."
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Juntas",
                    total_juntas
                )

            with col2:

                st.metric(
                    "Isométricos",
                    total_isometricos
                )

            with col3:

                st.metric(
                    "Soldadores",
                    total_soldadores
                )

            st.divider()

            st.warning(
                f"""
⚠ Atenção

Projeto: {projeto}

As juntas existentes serão removidas e substituídas pelos dados deste arquivo.
"""
            )

            confirmar = st.button(
                "🚀 Confirmar Importação",
                use_container_width=True
            )

            if confirmar:

                with st.spinner(
                    "Importando Weld List..."
                ):

                    projeto_id = projeto_dict[projeto]

                    excluir_juntas_projeto(
                        projeto_id
                    )

                    importar_dataframe_juntas(
                        df,
                        projeto_id
                    )

                    total_importado = (
                        contar_juntas_projeto(
                            projeto_id
                        )
                    )

                st.success(
                    f"""
Importação concluída!

Projeto: {projeto}

Juntas importadas: {total_importado}
"""
                )

        except Exception as e:

            st.error(
                f"Erro ao processar arquivo: {e}"
            )