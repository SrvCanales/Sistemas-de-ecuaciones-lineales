import streamlit as st
import streamlit.components.v1 as components
from frontend.ai_matrix_solver import generar_pdf_con_gemini 
import os
import time

st.cache_data.clear()
st.cache_resource.clear()

st.set_page_config(
    page_title="Guía - Sistemas de ecuaciones lineales",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ruta_frontend = os.path.join(os.path.dirname(__file__), "frontend")

# 1. Definimos la llave directamente en una variable
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Falta la llave GEMINI_API_KEY en los secretos.")
    st.stop()


# --- SISTEMA DE MEMORIA (CACHÉ) ---
if 'ultima_matriz' not in st.session_state:
    st.session_state.ultima_matriz = None
if 'ultimo_pdf' not in st.session_state:
    st.session_state.ultimo_pdf = None
if 'mensaje_error' not in st.session_state:
    st.session_state.mensaje_error = ""

# --- CARGA DE INTERFAZ GRÁFICA ---
try:
    visualizador_planos = components.declare_component(
        "visualizador_planos",
        path=ruta_frontend
    )
    
    # IMPORTANTE: Le añadimos un 'key' para que Streamlit mantenga estable la memoria de la interfaz
    matriz_recibida = visualizador_planos(key="interfaz_principal") 
    
except Exception as e:
    st.error(f"Error cargando la interfaz gráfica: {e}")
    matriz_recibida = None

# --- LÓGICA DE IA Y REINTENTOS ---
datos_recibidos = matriz_recibida # Renombramos para mayor claridad

if datos_recibidos is not None:
    # Extraemos las dos piezas del diccionario que envió JS
    matriz_actual = datos_recibidos["matriz"]
    solucion_esperada = datos_recibidos["solucion"]
    
    if matriz_actual != st.session_state.ultima_matriz:
        st.session_state.ultima_matriz = matriz_actual
        st.session_state.ultimo_pdf = None
        
        st.info("Generando explicación detallada con IA... Esto puede tardar unos segundos.")
        
        with st.spinner('Procesando matemáticas y compilando PDF...'):
            max_intentos = 3
            for intento in range(max_intentos):
                # Le pasamos AMBOS datos a tu función
                pdf_gen, error_msg = generar_pdf_con_gemini(matriz_actual, solucion_esperada, GEMINI_API_KEY)
                # ... (el resto del bucle se mantiene igual)
                
                if pdf_gen is not None:
                    st.session_state.ultimo_pdf = pdf_gen
                    st.session_state.mensaje_error = ""
                    break # Éxito, salimos del bucle
                else:
                    st.session_state.mensaje_error = error_msg
                    time.sleep(3) # Pausa antes de reintentar

    # --- RESULTADO ---
    if st.session_state.ultimo_pdf:
        st.success("¡Procedimiento generado con éxito!")
        st.download_button(
            label="📄 Descargar Procedimiento (PDF)",
            data=st.session_state.ultimo_pdf,
            file_name="Resolucion_Sistema_Lineal.pdf",
            mime="application/pdf"
            # (Eliminamos el on_click problemático de aquí)
        )
    elif st.session_state.mensaje_error:
        st.error(f"Hubo un problema tras varios intentos automáticos. Error técnico: {st.session_state.mensaje_error}")
