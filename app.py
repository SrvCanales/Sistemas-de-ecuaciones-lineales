import streamlit as st

# 1. Configuración Global (Debe ser la primera línea de toda la aplicación)
st.set_page_config(
    page_title="Laboratorio Matemático",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inicializar el enrutador en la memoria
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'inicio'

def cambiar_pagina(nueva_pagina):
    st.session_state.pagina_actual = nueva_pagina
    st.rerun()

# 3. LÓGICA DE NAVEGACIÓN
if st.session_state.pagina_actual == 'inicio':
    
    # --- ESTILOS DEL MENÚ (Inyectados solo aquí) ---
    st.markdown("""
    <style>
    /* Fondo principal y textos */
    .stApp { background-color: #12141c; }
    h1 { color: #eeeae2; font-family: 'Newsreader', serif; text-align: center; margin-top: 4rem; font-size: 3rem;}
    .subtitulo { color: #8c92a4; text-align: center; font-size: 1.2rem; margin-bottom: 5rem; }
    
    /* Diseño de las "Tarjetas" (Botones gigantes de Streamlit) */
    div.stButton > button {
        background-color: #181b26;
        color: #eeeae2;
        border: 1px solid #272b3a;
        border-radius: 12px;
        padding: 4rem 1rem;
        font-size: 1.5rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Efecto Hover interactivo */
    div.stButton > button:hover {
        border-color: #e8b94e;
        color: #e8b94e;
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(232, 185, 78, 0.15);
    }
    
    /* Ocultar barra superior decorativa de Streamlit */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    # --- INTERFAZ DEL MENÚ ---
    st.markdown("<h1>Laboratorio Matemático</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo'>Selecciona el entorno de simulación que deseas iniciar</p>", unsafe_allow_html=True)

    # Usamos columnas para centrar las dos opciones
    col1, col2, col3, col4 = st.columns([1, 4, 4, 1])

    with col2:
        if st.button("📐 Analizar sistemas de ecuaciones"):
            cambiar_pagina('sistemas')
            
    with col3:
        if st.button("🚀 Analizar geometría vectorial"):
            cambiar_pagina('vectores')

# --- ENRUTAMIENTO A LOS MÓDULOS ---
elif st.session_state.pagina_actual == 'sistemas':
    from modulos import app_sistemas
    app_sistemas.renderizar_aplicacion()

elif st.session_state.pagina_actual == 'vectores':
    from modulos import app_vectores
    app_vectores.renderizar_aplicacion()
