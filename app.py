import streamlit as st

from auth.login import autenticar

from modules.dashboard import render as dashboard_render
from modules.projetos import render as projetos_render
from modules.planejamento import render as planejamento_render
from modules.upload_weldlist import render as upload_render
from modules.rastreabilidade import render as rastreabilidade_render
from modules.producao import render as producao_render
from modules.qualidade import render as qualidade_render
from modules.relatorios import render as relatorios_render
from modules.configuracoes import render as configuracoes_render


st.set_page_config(
    page_title="WeldControl",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None


def tela_login():

    with st.sidebar:

        st.markdown("## ⚙️ WeldControl")
        st.caption("Controle de Soldas")

        st.divider()

        st.markdown("### 🔒 Acesso ao Sistema")

        usuario = st.text_input(
            "Usuário",
            placeholder="Digite seu usuário"
        )

        senha = st.text_input(
            "Senha",
            type="password",
            placeholder="Digite sua senha"
        )

        entrar = st.button(
            "Entrar",
            use_container_width=True
        )

        st.divider()

        st.caption("v1.0.0")

    st.title("⚙️ WeldControl")

    st.info(
        "Sistema corporativo para gestão de soldagem, inspeção e rastreabilidade."
    )

    if entrar:

        user = autenticar(usuario, senha)

        if user:

            st.session_state.usuario_logado = {
                "usuario": user.usuario,
                "perfil": user.perfil
            }

            st.rerun()

        else:

            st.error("Usuário ou senha inválidos")


def tela_principal():

    with st.sidebar:

        st.markdown("## ⚙️ WeldControl")
        st.caption("Controle de Soldas")

        st.divider()

        st.success(
            f"👤 {st.session_state.usuario_logado['usuario']}"
        )

        st.info(
            f"🛡️ {st.session_state.usuario_logado['perfil']}"
        )

        if st.button(
            "🚪 Sair",
            use_container_width=True
        ):
            st.session_state.usuario_logado = None
            st.rerun()

        st.divider()

        st.caption("v1.0.0")

    perfil = st.session_state.usuario_logado["perfil"]

    if perfil == "Administrador":

        abas = st.tabs([
            "📊 Dashboard",
            "📁 Projetos",
            "📐 Planejamento",
            "📤 Upload Weld List",
            "🔎 Rastreabilidade",
            "📋 Produção",
            "🛡️ Qualidade",
            "📈 Relatórios",
            "⚙️ Configurações"
        ])

        with abas[0]:
            dashboard_render()

        with abas[1]:
            projetos_render()

        with abas[2]:
            planejamento_render()

        with abas[3]:
            upload_render()

        with abas[4]:
            rastreabilidade_render()

        with abas[5]:
            producao_render()

        with abas[6]:
            qualidade_render()

        with abas[7]:
            relatorios_render()

        with abas[8]:
            configuracoes_render()

    else:

        abas = st.tabs([
            "📊 Dashboard",
            "🔎 Rastreabilidade",
            "📋 Produção",
            "🛡️ Qualidade",
            "📈 Relatórios"
        ])

        with abas[0]:
            dashboard_render()

        with abas[1]:
            rastreabilidade_render()

        with abas[2]:
            producao_render()

        with abas[3]:
            qualidade_render()

        with abas[4]:
            relatorios_render()


if st.session_state.usuario_logado is None:
    tela_login()
else:
    tela_principal()