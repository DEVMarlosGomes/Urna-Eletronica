import streamlit as st
from PIL import Image
import os

# --- Configurações de estilo customizadas via CSS ---
def style_page():
    st.markdown(
        """
        <style>
        /* Fundo branco amarelado */
        .main {
            background-color: #fffde7;
            padding: 20px;
            border-radius: 10px;
            max-width: 700px;
            margin: auto;
        }
        /* Faixa vertical direita com 4 listras da bandeira do Brasil */
        .sidebar .css-1d391kg {
            background: linear-gradient(
                to bottom,
                #009b3a 25%,   /* verde */
                #fedf00 25%, #fedf00 50%, /* amarelo */
                #002776 50%, #002776 75%, /* azul */
                #ff0000 75%, #ff0000 100% /* vermelho para simular vermelho (não é da bandeira, só p/ efeito) */
            );
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

style_page()

# --- Dados globais ---
if "candidatos" not in st.session_state:
    st.session_state.candidatos = []
if "votacao_ativa" not in st.session_state:
    st.session_state.votacao_ativa = False
if "numero_voto" not in st.session_state:
    st.session_state.numero_voto = ""
if "votos_brancos" not in st.session_state:
    st.session_state.votos_brancos = 0
if "votos_nulos" not in st.session_state:
    st.session_state.votos_nulos = 0


# --- Funções ---
def salvar_candidato(numero, nome, partido, imagem_file):
    # Verifica duplicidade
    for c in st.session_state.candidatos:
        if c["numero"] == numero:
            st.error("Número já cadastrado.")
            return False
    # Salva imagem localmente
    caminho_imagem = None
    if imagem_file is not None:
        os.makedirs("imagens", exist_ok=True)
        caminho_imagem = f"imagens/{numero}.png"
        with open(caminho_imagem, "wb") as f:
            f.write(imagem_file.getbuffer())
    st.session_state.candidatos.append({
        "numero": numero,
        "nome": nome,
        "partido": partido,
        "votos": 0,
        "imagem": caminho_imagem
    })
    st.success("Candidato cadastrado com sucesso!")
    return True


def mostrar_candidatos():
    st.subheader("Candidatos cadastrados:")
    for c in st.session_state.candidatos:
        cols = st.columns([1, 3, 3, 3])
        if c["imagem"] and os.path.exists(c["imagem"]):
            img = Image.open(c["imagem"]).resize((70,70))
            cols[0].image(img)
        else:
            cols[0].write("Sem imagem")
        cols[1].write(f"**Número:** {c['numero']}")
        cols[2].write(f"**Nome:** {c['nome']}")
        cols[3].write(f"**Partido:** {c['partido']}")


def mostrar_resultado():
    st.title("Resultado da Votação")
    total_votos = sum(c["votos"] for c in st.session_state.candidatos) + st.session_state.votos_brancos + st.session_state.votos_nulos
    if total_votos == 0:
        st.warning("Nenhum voto registrado.")
        return

    for c in st.session_state.candidatos:
        st.write(f"**{c['nome']} ({c['partido']})**: {c['votos']} votos")

    st.write(f"Votos em branco: {st.session_state.votos_brancos}")
    st.write(f"Votos nulos: {st.session_state.votos_nulos}")

    vencedor = max(st.session_state.candidatos, key=lambda x: x["votos"])
    st.success(f"Candidato vencedor: {vencedor['nome']} ({vencedor['partido']}) com {vencedor['votos']} votos.")


def reset_votacao():
    st.session_state.numero_voto = ""
    st.session_state.votos_brancos = 0
    st.session_state.votos_nulos = 0
    for c in st.session_state.candidatos:
        c["votos"] = 0


# --- Interface principal ---
st.markdown('<div class="main">', unsafe_allow_html=True)

menu = st.sidebar.selectbox(
    "Menu",
    ["Cadastro de Candidatos", "Votação", "Encerrar Votação / Resultado"]
)

if menu == "Cadastro de Candidatos":
    st.title("Cadastro de Candidatos")

    with st.form("form_cadastro"):
        numero = st.text_input("Número do candidato")
        nome = st.text_input("Nome do candidato")
        partido = st.text_input("Partido")
        imagem_file = st.file_uploader("Imagem do candidato (PNG ou JPG)", type=["png", "jpg", "jpeg"])
        enviar = st.form_submit_button("Cadastrar")

        if enviar:
            if not numero or not nome or not partido:
                st.error("Preencha todos os campos.")
            else:
                if salvar_candidato(numero, nome, partido, imagem_file):
                    st.experimental_rerun()

    if st.session_state.candidatos:
        mostrar_candidatos()

elif menu == "Votação":
    st.title("Urna Eletrônica - Votação")

    if not st.session_state.candidatos:
        st.warning("Nenhum candidato cadastrado. Cadastre antes de iniciar a votação.")
    else:
        st.write("Digite o número do candidato:")

        # Mostra o campo do número via botões tipo teclado numérico
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        col7, col8, col9 = st.columns(3)
        col0, col_b, col_c = st.columns(3)

        def btn_click(x):
            st.session_state.numero_voto += str(x)

        for i, col in enumerate([col1, col2, col3, col4, col5, col6, col7, col8, col9]):
            with col:
                st.button(str(i+1), on_click=btn_click, args=(i+1,))

        with col0:
            st.button("0", on_click=btn_click, args=(0,))
        with col_b:
            st.button("Branco", key="btn_branco")
        with col_c:
            st.button("Corrigir", key="btn_corrigir")

        # Mostrar o número digitado
        st.text_input("Número do candidato", value=st.session_state.numero_voto, disabled=True)

        # Mostra imagem do candidato ou vazio
        candidato = next((c for c in st.session_state.candidatos if c["numero"] == st.session_state.numero_voto), None)
        if candidato:
            st.image(candidato["imagem"], width=150)
            st.write(f"Nome: {candidato['nome']}")
            st.write(f"Partido: {candidato['partido']}")
        else:
            if st.session_state.numero_voto:
                st.write("Número inválido ou inexistente.")

        # Botões Confirmar voto
        col_confirmar, col_reset = st.columns(2)
        with col_confirmar:
            if st.button("Confirmar Voto"):
                if st.session_state.numero_voto == "":
                    st.warning("Digite o número do candidato ou selecione Branco.")
                else:
                    if st.session_state.numero_voto.lower() == "branco":
                        st.session_state.votos_brancos += 1
                        st.success("Voto em branco registrado!")
                    elif candidato:
                        candidato["votos"] += 1
                        st.success(f"Voto registrado para {candidato['nome']}!")
                    else:
                        st.session_state.votos_nulos += 1
                        st.success("Voto nulo registrado!")
                    st.session_state.numero_voto = ""
                    st.experimental_rerun()
        with col_reset:
            if st.button("Corrigir"):
                st.session_state.numero_voto = ""
                st.experimental_rerun()

elif menu == "Encerrar Votação / Resultado":
    st.title("Encerrar Votação / Resultado")
    if st.button("Encerrar Votação"):
        if st.session_state.candidatos:
            st.session_state.votacao_ativa = False
            mostrar_resultado()
        else:
            st.warning("Nenhum candidato cadastrado.")
    else:
        mostrar_resultado()

st.markdown("</div>", unsafe_allow_html=True)
