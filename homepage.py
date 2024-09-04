import streamlit as st

st.title("Homepage")

evidence_analyzer_page = st.Page("evidence_analyzer.py", title="Evidence Analyzer")
data_story_page = st.Page("data_story_helper.py", title="Data Story Helper")

pg = st.navigation([evidence_analyzer_page, data_story_page])
pg.run()
