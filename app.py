import streamlit as st
import streamlit.components.v1 as components
from frontend.ai_matrix_solver import generar_pdf_con_gemini 
import os

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

# 3. Lógica de generación del PDF
if matriz_recibida is not None:
    st.info("Generando explicación detallada con IA... Esto puede tardar unos segundos.")
    
    with st.spinner('Procesando matemáticas y compilando PDF...'):
        # Ahora recibimos dos variables
        pdf_generado, mensaje_error = generar_pdf_con_gemini(matriz_recibida, GEMINI_API_KEY)
        
    if pdf_generado:
        st.success("¡Procedimiento generado con éxito!")
        st.download_button(
            label="Descargar Procedimiento (PDF)",
            data=pdf_generado,
            file_name="Resolucion_Sistema_Lineal.pdf",
            mime="application/pdf"
        )
    else:
        # Aquí veremos exactamente qué fue lo que colapsó
        st.error(f"Hubo un problema al generar el PDF. Error técnico: {mensaje_error}")
