import streamlit as st

st.title("Evidence Analyzer")

tab_titles = ["tab1", "tab2"]
tab = st.tabs(tab_titles)

test = st.text_input("..")

tab_titles.append(test)
