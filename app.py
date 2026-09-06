import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Guía - Sistemas de ecuaciones lineales",
    layout="wide",
    initial_sidebar_state="collapsed"
)

HTML_FILE = BASE_DIR / "frontend" / "index.html"

# 1. Declarar el componente conectándolo a la carpeta 'frontend'
# Esto crea una función que renderizará tu HTML y retornará lo que JS envíe
visualizador_planos = components.declare_component(
    "visualizador_planos",
    path="frontend" # La carpeta que creamos en el Paso 1
)

# 2. Mostrar la interfaz y capturar el resultado
# El valor será 'None' hasta que el usuario presione el botón PDF
matriz_recibida = visualizador_planos()
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()
# 3. Lógica de la IA (Se ejecuta cuando JS envía la matriz)
if matriz_recibida is not None:
    st.success("¡Matriz recibida exitosamente desde la interfaz gráfica!")
    
    # Aquí la matriz llega como una lista de listas estándar de Python
    # Ejemplo: [[1, 1, 1, 6], [1, -1, 2, 5], [2, 1, -1, 1]]
    st.write("Matriz a procesar por la IA:", matriz_recibida)
    
    # --- AQUÍ INYECTAS TU CÓDIGO DE IA ---
    # prompt = f"Resuelve paso a paso este sistema matricial: {matriz_recibida}"
    # respuesta_ia = modelo_ia.generar(prompt)
    # generar_pdf(respuesta_ia)
    # --------------------------------------
    
    # Botón nativo de Streamlit para descargar el PDF generado
    # st.download_button("Descargar PDF", data=archivo_pdf, file_name="resolucion.pdf")
