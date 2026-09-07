import streamlit as st
import streamlit.components.v1 as components
import sys
import os
from pathlib import Path
from frontend.ai_matrix_solver import generar_pdf_con_gemini 

st.set_page_config(
    page_title="Guía - Sistemas de ecuaciones lineales",
    layout="wide",
    initial_sidebar_state="collapsed"
)

headers = {"authorization": st.secrets["GEMINI_API_KEY"]}

BASE_DIR = Path(__file__).parent
HTML_FILE = BASE_DIR / "frontend" / "index.html"

try:
    visualizador_planos = components.declare_component(
    "visualizador_planos",
    path="frontend" 
)
    matriz_recibida = visualizador() # Aquí se guarda lo que JS envíe
except Exception as e:
    st.error("Error cargando la interfaz gráfica.")
    matriz_recibida = None

if matriz_recibida is not None:
    st.info("Generando explicación detallada con IA... Esto puede tardar unos segundos.")
    
    with st.spinner('Procesando matemáticas y compilando PDF...'):
        # Llamamos a tu archivo solver
        pdf_generado = generar_pdf_con_gemini(matriz_recibida, GEMINI_API_KEY)
        
    if pdf_generado:
        st.success("¡Procedimiento generado con éxito!")
        # Botón nativo para que el usuario descargue el PDF
        st.download_button(
            label="Descargar Procedimiento (PDF)",
            data=pdf_generado,
            file_name="Resolucion_Sistema_Lineal.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Hubo un problema al generar el PDF.")
