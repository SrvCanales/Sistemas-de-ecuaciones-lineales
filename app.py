import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Guía - Sistemas de ecuaciones lineales",
    layout="wide",
    initial_sidebar_state="collapsed"
)

#Rutas
BASE_DIR = Path(__file__).parent
HTML_FILE = BASE_DIR / "components" / "base.html"


with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

components.html(
    html,
    height=1000,
    scrolling=False
)
