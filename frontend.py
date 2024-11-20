import streamlit as st

# Paleta de colores y rutas de los logos
PRIMARY_COLOR = "#4b83c0"
SECONDARY_COLOR = "#878889"
BACKGROUND_COLOR = "#f4f5f7"

ICOMEX_LOGO_PATH = "logos/ICOMEX_Logos sin fondo.png"
SOFIA_LOGO_PATH = "logos/SofIA sin fondo.png"

# Estilo personalizado
def render_custom_styles():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {BACKGROUND_COLOR};
            }}
            .title {{
                color: {PRIMARY_COLOR};
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }}
            .stButton>button {{
                background-color: {SECONDARY_COLOR};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
                transition: background-color 0.3s ease;
            }}
            .stButton>button:hover {{
                background-color: {PRIMARY_COLOR};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Renderizar encabezado con logos lado a lado
def render_title():
    logo_col1, logo_col2 = st.columns([1, 5], gap="medium")
    with logo_col1:
        st.image(SOFIA_LOGO_PATH, use_container_width=True)
    with logo_col2:
        st.image(ICOMEX_LOGO_PATH, use_container_width=True)

    # Título principal con color personalizado
    st.markdown('<div class="title">Sofía, asistente virtual</div>', unsafe_allow_html=True)

# Funciones de selección
def select_investment():
    st.session_state.selected_topic = "Oportunidades de Inversión"
    st.session_state.initial_message = (
        "¡Hola! Soy Sofía, la asistente virtual de I-COMEX 😊. "
        "Parece que te interesan las oportunidades de inversión en La Pampa. "
        "Decime, ¿hay algo en particular que quisieras saber?"
    )
    st.session_state.initial_message_shown = False

def select_export():
    st.session_state.selected_topic = "Exportación de Servicios"
    st.session_state.initial_message = (
        "¡Hola! Soy Sofía, la asistente virtual de I-COMEX 😊. "
        "¿Estás planificando exportar tus servicios? "
        "Contame un poco más sobre lo que te gustaría saber."
    )
    st.session_state.initial_message_shown = False

# Renderizar la introducción y los botones iniciales
def render_intro():
    st.markdown(
        """
        Soy **Sofía**, el agente de IA de la Agencia I-COMEX. Estoy aquí para ayudarte con tus preguntas
        sobre comercio exterior e inversiones en La Pampa.

        ¿Sobre qué tema necesitás ayuda?
        """
    )

    # Botones con funciones de devolución de llamada
    btn_col1, btn_col2 = st.columns(2, gap="large")
    inversiones_btn = btn_col1.button(
        "Oportunidades de Inversión", 
        key="intro_inversiones", 
        on_click=select_investment
    )
    comercio_btn = btn_col2.button(
        "Exportación de Servicios", 
        key="intro_comercio", 
        on_click=select_export
    )

# Renderizar subtítulo
def render_subheader(topic):
    st.subheader(topic.capitalize())

# Renderizar mensajes
def render_messages(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Renderizar campo de entrada
def render_input():
    return st.chat_input("Escribe tu mensaje aquí...")
