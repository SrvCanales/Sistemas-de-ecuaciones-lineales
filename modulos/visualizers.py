"""Visualizadores interactivos para Streamlit: producto punto, producto cruz y cosenos directores.

Cada visualizador es un componente HTML autocontenido (canvas + panel de valores) que vive en
`components/`. Se renderiza con `st.components.v1.html`, de modo que arrastrar los vectores
actualiza la vista y los números al instante, sin recargar el script de Streamlit.

En pantallas estrechas (móvil) el componente se apila en una columna y ajusta su propia altura.
"""
from pathlib import Path

import streamlit.components.v1 as components

_DIR = Path(__file__).parent / "components"

# Marcadores que cada HTML deja para recibir el CSS y las utilidades JS compartidas.
_SLOTS = {"/*__BASE_CSS__*/": "base.css", "/*__COMMON_JS__*/": "common.js"}


def _load(name: str) -> str:
    html = (_DIR / name).read_text(encoding="utf-8")
    for slot, filename in _SLOTS.items():
        html = html.replace(slot, (_DIR / filename).read_text(encoding="utf-8"))
    return html


def dot_product_visualizer(height: int = 660) -> None:
    """Producto punto en R2: ángulo θ, proyección y A·B = |A||B|cos θ."""
    components.html(_load("dot_product.html"), height=height, scrolling=True)


def cross_product_visualizer(height: int = 800) -> None:
    """Producto cruz: vista 3D, plano de A y B, y |A×B| = |A||B|sin θ."""
    components.html(_load("cross_product.html"), height=height, scrolling=True)


def direction_cosines_visualizer(dim: int = 2, height: int | None = None) -> None:
    """Cosenos directores de un vector v en R2 (α, β) o en R3 (α, β, γ)."""
    if dim not in (2, 3):
        raise ValueError("dim debe ser 2 o 3")
    components.html(_load(f"cosines_{dim}d.html"), height=height or (660 if dim == 2 else 700), scrolling=True)
