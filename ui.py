"""Compatibilité entre versions de Streamlit.

Selon la version installée (Python 3.9 → Streamlit ≤ 1.50), chaque fonction n'accepte pas
les mêmes options de largeur. On inspecte donc la fonction elle-même avant de l'appeler.
"""
import inspect

import streamlit as st

_V = tuple(int(x) for x in st.__version__.split(".")[:2])


def stretch(fn):
    """Options pour qu'un élément prenne toute la largeur disponible."""
    p = inspect.signature(fn).parameters
    if "use_container_width" in p and _V < (1, 51):
        return {"use_container_width": True}
    if "width" in p and _V >= (1, 46):
        return {"width": "stretch"}
    if "use_container_width" in p:
        return {"use_container_width": True}
    if "use_column_width" in p:
        return {"use_column_width": True}
    return {}


def natural(fn):
    """Options pour qu'un élément garde sa largeur propre."""
    p = inspect.signature(fn).parameters
    if "use_container_width" in p and _V < (1, 51):
        return {"use_container_width": False}
    if "width" in p and _V >= (1, 46):
        return {"width": "content"}
    return {}


def chart(c, full=True):
    """Affiche un graphique Altair, quelle que soit la version de Streamlit."""
    st.altair_chart(c, **(stretch(st.altair_chart) if full else natural(st.altair_chart)))


def button(container, label, **kw):
    """Bouton pleine largeur."""
    return container.button(label, **kw, **stretch(st.button))


def image(container, img, **kw):
    return container.image(img, **kw, **stretch(st.image))
