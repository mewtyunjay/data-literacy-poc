import streamlit as st
from streamlit import session_state as ss

# print(f"session state {ss.country}")

print("processor")
st.write("Test")
# http://localhost:8501/processor/?country=Manila
country = st.query_params.get("country", None)

st.write(f'Processing {country} ...')
