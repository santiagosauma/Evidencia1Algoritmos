import re
import streamlit as st
from kmp import kmp_search
from lcs import lcs
from manacher import manacher
from tries import Trie

trie = Trie()

st.set_page_config(page_title="Actividad Integradora 1", layout="centered")

st.markdown("# E1. Actividad Integradora 1")
st.markdown("Isaac Hernández Pérez A01198674")
st.markdown("Luis Santiago Sauma Peñaloza A00836418")

text1 = ""
text2 = ""
clean_text1 = ""
clean_text2 = ""

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text)

def highlight_single_pattern(text, start, pattern):
    end = start + len(pattern)
    highlighted_text = (
        text[:start] + f"<span style='background-color: yellow'>{text[start:end]}</span>" + text[end:]
    )
    return highlighted_text

uploaded_files = st.file_uploader("Subir archivo(s) de texto", type="txt", accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) >= 1:
        text1 = uploaded_files[0].read().decode("utf-8")
        text1 = st.text_area("Contenido del primer archivo", text1, height=200)
        clean_text1 = clean_text(text1)
        for word in clean_text1.split():
            trie.insert(word)

    if len(uploaded_files) == 2:
        text2 = uploaded_files[1].read().decode("utf-8")
        text2 = st.text_area("Contenido del segundo archivo", text2, height=200)
        clean_text2 = clean_text(text2)

if 'active_window' not in st.session_state:
    st.session_state['active_window'] = None

if 'kmp_matches' not in st.session_state:
    st.session_state['kmp_matches'] = []

if 'current_match_index' not in st.session_state:
    st.session_state['current_match_index'] = 0

if 'pattern' not in st.session_state:
    st.session_state['pattern'] = ''

st.subheader("Opciones")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Buscar"):
        st.session_state['active_window'] = 'buscar'

with col2:
    if clean_text1 and clean_text2:
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
    pattern = st.text_input("Ingresar patrón para buscar (KMP):", value=st.session_state['pattern'])

    if st.button("Buscar patrón"):
        if pattern.strip():
            st.session_state['pattern'] = pattern
            st.session_state['kmp_matches'] = kmp_search(text1, st.session_state['pattern'])
            st.session_state['current_match_index'] = 0

            if not st.session_state['kmp_matches']:
                st.write("No se encontraron coincidencias.")
        else:
            st.warning("Por favor, ingrese un patrón para buscar.")

    if st.session_state['kmp_matches']:
        def prev_match():
            if st.session_state['current_match_index'] > 0:
                st.session_state['current_match_index'] -= 1

        def next_match():
            if st.session_state['current_match_index'] < len(st.session_state['kmp_matches']) - 1:
                st.session_state['current_match_index'] += 1

        col_prev, col_next = st.columns([1, 1])

        with col_prev:
            st.button("Retroceder", disabled=(st.session_state['current_match_index'] == 0), on_click=prev_match, key='prev_button')

        with col_next:
            st.button("Avanzar", disabled=(st.session_state['current_match_index'] == len(st.session_state['kmp_matches']) - 1), on_click=next_match, key='next_button')

        current_index = st.session_state['current_match_index']
        start = st.session_state['kmp_matches'][current_index]

        if start >= 0:
            highlighted_text1 = highlight_single_pattern(text1, start, st.session_state['pattern'])
            st.markdown(f"**Texto 1 con coincidencia resaltada:**")
            st.markdown(highlighted_text1, unsafe_allow_html=True)

if st.session_state['active_window'] == 'similitud':
    st.subheader("Similitud entre dos textos")
    if clean_text1 and clean_text2:
        common_substrings = lcs(clean_text1, clean_text2)
        if common_substrings:
            highlighted_text1 = text1
            highlighted_text2 = text2
            for substring in common_substrings:
                highlighted_text1 = highlighted_text1.replace(substring, f"<span style='background-color: lightblue'>{substring}</span>")
                highlighted_text2 = highlighted_text2.replace(substring, f"<span style='background-color: lightblue'>{substring}</span>")
            st.markdown(f"**Subcadena(s) común más larga:** {', '.join(common_substrings)}")
            st.markdown(f"**Texto 1:** {highlighted_text1}", unsafe_allow_html=True)
            st.markdown(f"**Texto 2:** {highlighted_text2}", unsafe_allow_html=True)
        else:
            st.write("No hay subcadena común entre los textos.")

if st.session_state['active_window'] == 'palindromo':
    st.subheader("Palíndromo más largo")
    palindromo = manacher(clean_text1)
    
    if palindromo:
        start_index = text1.find(palindromo)
        if start_index != -1:
            highlighted_text = (text1[:start_index] + 
                                f"<span style='background-color: lightgreen'>{palindromo}</span>" + 
                                text1[start_index + len(palindromo):])
            st.markdown(highlighted_text, unsafe_allow_html=True)
        else:
            st.write("No se encontró un palíndromo.")
    else:
        st.write("No se encontró un palíndromo.")

if st.session_state['active_window'] == 'autocompletar':
    st.subheader("Autocompletar")
    prefix = st.text_input("Escribe para autocompletar:")

    if prefix:
        suggestions = trie.search(clean_text(prefix))
        if suggestions:
            st.write("Sugerencias:")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
        else:
            st.write("No se encontraron sugerencias.")