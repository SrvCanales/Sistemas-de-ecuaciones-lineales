import streamlit as st
import streamlit.components.v1 as components
import os

def renderizar_aplicacion():
    # 1. Botón para volver al menú
    if st.button("⬅ Volver al Menú Principal"):
        st.session_state.pagina_actual = 'inicio'
        st.rerun()
        
    st.markdown("<hr>", unsafe_allow_html=True) # Separador visual

    dir_actual = os.path.dirname(__file__)
    ruta_frontend = os.path.abspath(os.path.join(dir_actual, "..", "frontend", "sistemas"))
    
    # ... resto del código ...

    from .visualizers import (
        cross_product_visualizer,
        direction_cosines_visualizer,
        dot_product_visualizer,
    )
    
    st.set_page_config(page_title="Producto punto, producto cruz y cosenos directores", page_icon="◢", layout="wide")
    
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&display=swap');
    
        :root{ --bg:#12141c; --panel:#181b26; --panel-line:#272b3a; --text:#eeeae2; --muted:#8c92a4; --sol:#e8b94e; }
    
        html, body, .stApp, [data-testid="stAppViewContainer"]{ background:var(--bg); font-family:'Figtree',system-ui,sans-serif; }
        [data-testid="stHeader"]{ background:transparent; }
        #MainMenu, footer{ visibility:hidden; }
        .block-container{ max-width:1320px; padding-top:2.4rem; padding-bottom:2rem; }
    
        .titulo{ font-family:'Newsreader',Georgia,serif; font-size:2.3rem; line-height:1.15; color:var(--text); margin:0 0 .3rem; }
        .subtitulo{ color:var(--muted); font-size:1.02rem; margin:0 0 1.4rem; max-width:60ch; }
    
        .stTabs [data-baseweb="tab-list"]{ gap:1.6rem; border-bottom:1px solid var(--panel-line); overflow-x:auto; }
        .stTabs [data-baseweb="tab"]{ padding:.5rem 0; color:var(--muted); background:transparent; white-space:nowrap; }
        .stTabs [aria-selected="true"]{ color:var(--text); }
        .stTabs [data-baseweb="tab-highlight"]{ background:var(--sol); height:2px; }
        .stTabs [data-baseweb="tab-border"]{ display:none; }
    
        /* selector R² / R³ */
        [data-testid="stSegmentedControl"] button, [data-testid="stRadio"] label{ font-family:'Figtree',system-ui,sans-serif; }
        [data-testid="stRadio"] [role="radiogroup"]{ gap:1.2rem; }
    
        .idea{ color:var(--muted); font-size:.98rem; line-height:1.6; max-width:78ch; margin:.9rem 0 0; }
        .idea b{ color:var(--text); font-weight:500; }
        iframe{ border:0; border-radius:14px; }
    
        @media (max-width: 640px){
          .block-container{ padding:1.1rem .7rem 1.5rem; }
          .titulo{ font-size:1.65rem; }
          .subtitulo{ font-size:.95rem; margin-bottom:1rem; }
          .stTabs [data-baseweb="tab-list"]{ gap:1.1rem; }
          .idea{ font-size:.93rem; }
        }
        </style>
        <h1 class="titulo">Producto punto, producto cruz y cosenos directores</h1>
        <p class="subtitulo">Mueve los vectores y observa qué le pasa al ángulo, a la proyección y al área.</p>
        """,
        unsafe_allow_html=True,
    )
    
    tab_dot, tab_cross, tab_cos = st.tabs(["Producto punto", "Producto cruz", "Cosenos directores"])
    
    with tab_dot:
        dot_product_visualizer(height=660)
        st.markdown(
            '<p class="idea">El producto punto <b>mide cuánto apunta un vector en la dirección del otro</b>. '
            "Proyecta uno sobre el otro y multiplica esa componente por la longitud del vector base: "
            "es positivo si el ángulo es agudo, cero si son perpendiculares y negativo si es obtuso.</p>",
            unsafe_allow_html=True,
        )
    
    with tab_cross:
        cross_product_visualizer(height=800)
        st.markdown(
            '<p class="idea">El producto cruz <b>construye un vector perpendicular a los dos originales</b>. '
            "Su longitud es el área del paralelogramo que forman, así que vale cero cuando son paralelos "
            "y es máxima cuando son perpendiculares. El sentido lo da la regla de la mano derecha. "
            "En el plano de la derecha solo giras los vectores dentro de su propio plano; para inclinarlo, usa la vista 3D.</p>",
            unsafe_allow_html=True,
        )
    
    with tab_cos:
        opciones = ["Visualizar en R²", "Visualizar en R³"]
        if hasattr(st, "segmented_control"):
            espacio = st.segmented_control("Espacio", opciones, default=opciones[0], label_visibility="collapsed")
        else:  # versiones antiguas de Streamlit
            espacio = st.radio("Espacio", opciones, horizontal=True, label_visibility="collapsed")
        dim = 3 if espacio == opciones[1] else 2
    
        direction_cosines_visualizer(dim=dim)
        st.markdown(
            '<p class="idea">Los cosenos directores son <b>los cosenos de los ángulos que un vector forma con los ejes</b>. '
            "Cada uno indica qué fracción de la longitud del vector cae sobre ese eje, y juntos forman el vector "
            "unitario que apunta en su misma dirección. Por eso la suma de sus cuadrados siempre es 1.</p>",
            unsafe_allow_html=True,
        )
