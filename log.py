import streamlit as st
import json
import hashlib
import os
import main

st.set_page_config(
    page_title='Rental Dash',
    page_icon='🛠️',
    layout='wide'
)

# Funções auxiliares
def carregar_dados():
    if not os.path.exists("usuarios.json"):
        # Arquivo inicial
        with open("usuarios.json", "w") as f:
            json.dump({"autorizados": [], "usuarios": {}}, f, indent=4)
    with open("usuarios.json", "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open("usuarios.json", "w") as f:
        json.dump(dados, f, indent=4)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Inicializa estado de sessão
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.email = ""
    st.session_state.nome = ""

# Ocultar sidebar e menus se estiver logado
if st.session_state.logado:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    main.show()

else:
    #%% logo
    st.markdown("""
        <style>
        .streamlit-expanderHeader {
            border-radius: 0 !important;
        }
        img {
            border-radius: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    # Injetar CSS para alinhar a imagem à direita
    st.markdown("""
        <style>
        .right-align {
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="right-align">', unsafe_allow_html=True)
    st.image('assets/imgs/logoHilti.png')
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("Rental Dash Login")
    dados = carregar_dados()

    pagina = st.sidebar.selectbox("Acesso", ["Login", "Cadastro"])

    if pagina == "Cadastro":
        st.subheader("Criar nova conta")
        email = st.text_input("Email")
        nome = st.text_input("Nome")
        senha = st.text_input("Senha", type="password")
        confirmar = st.text_input("Confirmar senha", type="password")

        if st.button("Cadastrar"):
            if email not in dados["autorizados"]:
                st.error("Email não autorizado para cadastro.")
            elif email in dados["usuarios"]:
                st.warning("Este email já está cadastrado.")
            elif senha != confirmar:
                st.warning("As senhas não coincidem.")
            else:
                dados["usuarios"][email] = {
                    "nome": nome,
                    "senha_hash": hash_senha(senha)
                }
                salvar_dados(dados)
                st.success("Cadastro realizado com sucesso!")

    elif pagina == "Login":
        st.subheader("Login")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            usuario = dados["usuarios"].get(email)
            if usuario and usuario["senha_hash"] == hash_senha(senha):
                st.session_state.logado = True
                st.session_state.email = email
                st.session_state.nome = usuario["nome"]
                st.rerun()
            else:
                st.error("Credenciais inválidas.")
