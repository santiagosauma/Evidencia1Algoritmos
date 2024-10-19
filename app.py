import streamlit as st
from kmp import kmp_search

st.set_page_config(page_title="Actividad Integradora 1", layout="centered")

st.markdown("# E1. Actividad Integradora 1")

st.subheader("Cargar archivo o escribir texto")
option = st.radio("Selecciona una opción:", ("Cargar archivo", "Escribir texto manualmente"))

text = ""

if option == "Cargar archivo":
    uploaded_file = st.file_uploader("Cargar archivo de texto", type="txt")
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("Contenido del archivo", text, height=400)
else:
    # Aquí reducimos la altura del cuadro de texto manual
    text = st.text_area("Escribe el texto aquí:", height=200)

pattern = st.text_input("Ingresar patrón para buscar (KMP):")

def highlight_pattern(text, pattern, occurrences):
    highlighted_text = ""
    last_idx = 0
    for start in occurrences:
        highlighted_text += text[last_idx:start]
        highlighted_text += f"<span style='background-color: yellow'>{pattern}</span>"
        last_idx = start + len(pattern)
    highlighted_text += text[last_idx:]
    return highlighted_text

if st.button("Buscar patrón"):
    if pattern and text:
        occurrences = kmp_search(text, pattern)
        if occurrences:
            highlighted_text = highlight_pattern(text, pattern, occurrences)
            st.markdown(highlighted_text, unsafe_allow_html=True)
        else:
            st.write("No se encontraron coincidencias.")
    else:
        st.write("Por favor, ingrese un texto y un patrón.")
