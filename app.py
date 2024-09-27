import streamlit as st

st.set_page_config(
    page_title="Home Page",
    page_icon=":home:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("# Welcome to the Data Remix prototype!")

st.markdown("""
There are two main functionalities we would like to test here:

* Evidence Selector: this tool helps the student discuss evidences with one agent and gather insights from it. Once the discussion is done, the student has the option to save it.

* Data Story Helper: this tool helps the student to build a coherent story from the discussed evidences.

To achieve that, we are restricting this proof-of-concept to discuss only evidences related to Social Media Usage by Teenagers.

The buttons below will direct you to the two tools.
""")

es = st.button("Evidence Selector")
dsh = st.button("Data Story Helper")

if es:
    st.switch_page("pages/evidence_selector.py")

if dsh:
    st.switch_page("pages/data_story_helper.py")
