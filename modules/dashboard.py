import streamlit as st


def render():

    st.title("📊 Dashboard WeldControl")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de Juntas", 0)

    with col2:
        st.metric("Soldadas", 0)

    with col3:
        st.metric("LP", 0)

    with col4:
        st.metric("US", 0)

    st.info(
        "Dashboard aguardando importação da Weld List."
    )