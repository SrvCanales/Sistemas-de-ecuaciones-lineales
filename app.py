import streamlit as st
import streamlit.components.v1 as components
from frontend.ai_matrix_solver import generar_pdf_con_gemini 
import os
import time

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


# ---  SISTEMA DE MEMORIA (CACHÉ) ---
# Evita que el PDF se regenere desde cero al presionar "Descargar"
if 'ultima_matriz' not in st.session_state:
    st.session_state.ultima_matriz = None
if 'ultimo_pdf' not in st.session_state:
    st.session_state.ultimo_pdf = None
if 'mensaje_error' not in st.session_state:
    st.session_state.mensaje_error = ""

# --- . COMUNICACIÓN INVERSA CON HTML ---
# Función que se ejecuta tras descargar para reiniciar el frontend
def resetear_boton_html():
    st.session_state.enviar_reset = True

# Si hay orden de reiniciar, inyectamos un script invisible
if st.session_state.get('enviar_reset', False):
    components.html("<script>window.parent.postMessage({type: 'reset_pdf_button'}, '*');</script>", height=0)
    st.session_state.enviar_reset = False

# --- . CARGA DE INTERFAZ GRÁFICA ---

# 2. Declaramos e instanciamos el componente con el MISMO nombre
try:
    visualizador_planos = components.declare_component(
        "visualizador_planos",
        path=ruta_frontend
    )
    
    # Usamos el nombre correcto de la variable declarada arriba
    matriz_recibida = visualizador_planos() 
    
except Exception as e:
    # Ahora imprimimos el error real (e) por si ocurre algo más
    st.error(f"Error cargando la interfaz gráfica: {e}")
    matriz_recibida = None

# --- . LÓGICA DE IA Y REINTENTOS ---
if matriz_recibida is not None:
    # Solo generamos si la matriz ingresada es NUEVA o si el botón forzó el recálculo
    if matriz_recibida != st.session_state.ultima_matriz:
        st.session_state.ultima_matriz = matriz_recibida
        st.session_state.ultimo_pdf = None
        
        st.info("Generando explicación detallada con IA... Esto puede tardar unos segundos.")
        
        with st.spinner('Procesando matemáticas y compilando PDF...'):
            
            # BUCLE DE REINTENTOS: Intenta hasta 3 veces si la API está saturada
            max_intentos = 3
            for intento in range(max_intentos):
                pdf_gen, error_msg = generar_pdf_con_gemini(matriz_recibida, GEMINI_API_KEY)
                
                if pdf_gen is not None:
                    st.session_state.ultimo_pdf = pdf_gen
                    st.session_state.mensaje_error = ""
                    break # Éxito, salimos del bucle
                else:
                    st.session_state.mensaje_error = error_msg
                    time.sleep(3) # Pausa de 3 segundos antes del siguiente intento
        
        # Al terminar (con éxito o fallo), ordenamos al botón de JS que se desbloquee
        components.html("<script>window.parent.postMessage({type: 'reset_pdf_button'}, '*');</script>", height=0)

    # --- . RESULTADO ---
    # Mostramos el botón basado en lo que hay en memoria, para que la descarga sea instantánea
    if st.session_state.ultimo_pdf:
        st.success("¡Procedimiento generado con éxito!")
        st.download_button(
            label="Descargar Procedimiento (PDF)",
            data=st.session_state.ultimo_pdf,
            file_name="Resolucion_Sistema_Lineal.pdf",
            mime="application/pdf",
            on_click=resetear_boton_html # Resetea el HTML tras descargar
        )
    elif st.session_state.mensaje_error:
        st.error(f"Hubo un problema tras varios intentos automáticos. Error técnico: {st.session_state.mensaje_error}")
