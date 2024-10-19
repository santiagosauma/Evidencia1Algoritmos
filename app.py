import streamlit as st
from kmp import kmp_search
from lcs import lcs
from manacher import manacher
from tries import Trie

trie = Trie()

st.set_page_config(page_title="Actividad Integradora 1", layout="centered")

st.markdown("# E1. Actividad Integradora 1")

option = st.radio("Selecciona una opción:", ("Cargar archivo(s)", "Escribir texto(s)"))

text1 = ""
text2 = ""

if option == "Cargar archivo(s)":
    uploaded_files = st.file_uploader("Subir archivo(s) de texto", type="txt", accept_multiple_files=True)

    if uploaded_files:
        if len(uploaded_files) >= 1:
            text1 = uploaded_files[0].read().decode("utf-8")
            text1 = st.text_area("Contenido del primer archivo", text1, height=200)
            for word in text1.split():
                trie.insert(word)

        if len(uploaded_files) == 2:
            text2 = uploaded_files[1].read().decode("utf-8")
            text2 = st.text_area("Contenido del segundo archivo", text2, height=200)
else:
    text1 = st.text_area("Escribe el primer texto aquí:", height=200)
    text2 = st.text_area("Escribe el segundo texto aquí (opcional):", height=200)

if 'active_window' not in st.session_state:
    st.session_state['active_window'] = None

st.subheader("Opciones")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Buscar"):
        st.session_state['active_window'] = 'buscar'

with col2:
    if text1 and text2:
        if st.button("Similitud"):
            st.session_state['active_window'] = 'similitud'
    else:
        st.button("Similitud", disabled=True)

with col3:
    if st.button("Palíndromo"):
        st.session_state['active_window'] = 'palindromo'

with col4:
    if st.button("Autocompletar"):
        st.session_state['active_window'] = 'autocompletar'

if st.session_state['active_window'] == 'buscar':
    st.subheader("Buscar patrón")
    pattern = st.text_input("Ingresar patrón para buscar (KMP):", value=st.session_state.get('pattern', ''))

    if st.button("Buscar patrón"):
        st.session_state['pattern'] = pattern

        if st.session_state['pattern'] and text1:
            occurrences = kmp_search(text1, st.session_state['pattern'])
            if occurrences:
                highlighted_text1 = text1
                for i in sorted(occurrences, reverse=True):
                    highlighted_text1 = highlighted_text1[:i] + f"<span style='background-color: yellow'>{st.session_state['pattern']}</span>" + highlighted_text1[i + len(st.session_state['pattern']):]
                st.markdown(f"**Texto 1 con coincidencias resaltadas:**")
                st.markdown(highlighted_text1, unsafe_allow_html=True)
            else:
                st.write("No se encontraron coincidencias.")
        else:
            st.write("Por favor, ingrese un patrón.")

if st.session_state['active_window'] == 'similitud':
    st.subheader("Similitud entre dos textos")
    if text1 and text2:
        common_subsequence = lcs(text1, text2)
        if common_subsequence:
            highlighted_text1 = text1.replace(common_subsequence, f"<span style='background-color: lightblue'>{common_subsequence}</span>")
            highlighted_text2 = text2.replace(common_subsequence, f"<span style='background-color: lightblue'>{common_subsequence}</span>")
            st.markdown(f"**Subcadena común más larga:** {common_subsequence}")
            st.markdown(f"**Texto 1:** {highlighted_text1}", unsafe_allow_html=True)
            st.markdown(f"**Texto 2:** {highlighted_text2}", unsafe_allow_html=True)
        else:
            st.write("No hay subcadena común entre los textos.")

if st.session_state['active_window'] == 'palindromo':
    st.subheader("Palíndromo más largo")
    palindromo = manacher(text1)
    st.markdown(f"<span style='background-color: lightgreen'>{palindromo}</span>", unsafe_allow_html=True)

if st.session_state['active_window'] == 'autocompletar':
    st.subheader("Autocompletar")
    prefix = st.text_input("Escribe para autocompletar:")
    if prefix:
        suggestions = trie.search(prefix)
        if suggestions:
            st.write("Sugerencias:", suggestions)
        else:
            st.write("No se encontraron sugerencias.")
