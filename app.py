import streamlit as st

# 1. Configuración Global
st.set_page_config(
    page_title="Aplicación Interactiva - Álgebra lineal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inicializar el enrutador en la memoria
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'inicio'

def cambiar_pagina(nueva_pagina):
    st.session_state.pagina_actual = nueva_pagina
    st.rerun()

# 3. LÓGICA DE NAVEGACIÓN Y MENÚ PRINCIPAL
if st.session_state.pagina_actual == 'inicio':
    
    # --- ESTILOS AVANZADOS DEL MENÚ ---
    st.markdown("""
    <style>
    /* Variables de color de tu paleta */
    :root {
        --bg: #12141c;
        --panel: #181b26;
        --panel-line: #272b3a;
        --text: #eeeae2;
        --muted: #8c92a4;
        --sol: #e8b94e;
    }

    /* Fondo principal y textos */
    .stApp { background-color: var(--bg); }
    h1 { color: var(--text); font-family: 'Newsreader', serif; text-align: center; margin-top: 4rem; font-size: 3.5rem; font-weight: 500;}
    .subtitulo { color: var(--muted); text-align: center; font-size: 1.2rem; margin-bottom: 4rem; font-family: 'IBM Plex Sans', sans-serif;}
    
    /* Diseño de las Tarjetas (Botones gigantes) */
    div.stButton > button {
        background-color: var(--panel);
        color: var(--text);
        border: 1px solid var(--panel-line);
        border-radius: 16px;
        height: 320px; /* Altura imponente */
        width: 100%;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 20px;
    }
    
    /* Efecto Hover interactivo */
    div.stButton > button:hover {
        border-color: var(--sol);
        color: var(--sol);
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(232, 185, 78, 0.15);
    }

    /* Formato del texto dentro del botón */
    div.stButton > button p {
        font-size: 1.5rem;
        font-weight: 600;
        font-family: 'IBM Plex Sans', sans-serif;
        white-space: pre-wrap; /* Permite el salto de línea \n */
        text-align: center;
        margin: 0;
    }

    /* --- INYECCIÓN DE ÍCONOS VECTORIALES (SVG) --- */
    
    /* Ícono Módulo 1: Sistemas de Ecuaciones (Llave con 3 ecuaciones) */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button::before {
        content: "";
        display: block;
        width: 90px;
        height: 90px;
        margin-bottom: 10px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M8 6 H21 M8 12 H21 M8 18 H21'/%3E%3Cpath d='M6 4 C 4 4, 4 6, 4 8 C 4 11, 2 12, 2 12 C 2 12, 4 13, 4 16 C 4 18, 4 20, 6 20'/%3E%3C/svg%3E");
        background-size: cover;
        transition: transform 0.3s ease;
    }

    /* Ícono Módulo 2: Geometría Vectorial (Dos vectores y ángulo) */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button::before {
        content: "";
        display: block;
        width: 90px;
        height: 90px;
        margin-bottom: 10px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='4' y1='20' x2='20' y2='20'/%3E%3Cpolyline points='16 16 20 20 16 24'/%3E%3Cline x1='4' y1='20' x2='14' y2='5'/%3E%3Cpolyline points='9 7 14 5 15 10'/%3E%3Cpath d='M 10 20 A 6 6 0 0 0 8.5 13'/%3E%3C/svg%3E");
        background-size: cover;
        transition: transform 0.3s ease;
    }

    /* Animación del ícono al pasar el mouse */
    div.stButton > button:hover::before {
        transform: scale(1.15);
    }

    /* Ocultar elementos decorativos por defecto de Streamlit */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    # --- INTERFAZ DEL MENÚ ---
    st.markdown("<h1>Aplicación Interactiva - Álgebra lineal</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo'>Selecciona el concepto que deseas analizar</p>", unsafe_allow_html=True)

    margen_izq, col1, col2, margen_der = st.columns(4, gap="large")

    with col1:
        # El \n crea el salto de línea perfecto debajo de "Módulo X:"
        if st.button("Módulo 1:\nSistemas de ecuaciones",  use_container_width=True):
            cambiar_pagina('sistemas')
            
    with col2:
        if st.button("Módulo 2:\nGeometría vectorial\n:black[<small>~Sólo para PC~</small>]",  use_container_width=True):
            cambiar_pagina('vectores')

# --- ENRUTAMIENTO A LOS MÓDULOS ---
elif st.session_state.pagina_actual == 'sistemas':
    from modulos import app_sistemas
    app_sistemas.renderizar_aplicacion()

elif st.session_state.pagina_actual == 'vectores':
    from modulos import app_vectores
    app_vectores.renderizar_aplicacion()
