import ollama
import streamlit as st

model = "llama3.1"
ollama.pull(model)

st.title("Data literacy chatbot")
st.caption(f"A Streamlit chatbot powered by {model}")

with st.sidebar:
    # st.sidebar.title("Resources")
    "[View the source code](https://github.com/mewtyunjay/data-literacy-poc)"

st.write("Let's start! First, fill the box below with your thesis and beliefs on the topic")

main_thesis = st.text_input(label="Thesis", placeholder="Example: I believe that teenagers should not use social media because it is hurtful")
main_topic = "Social media usage by teenagers"

welcome_message = f"Ok, so you need to build an argument about {main_topic} and your starting point of view is \"{main_thesis}\""

if main_thesis != "":
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": f"{welcome_message}. How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = ollama.chat(model=model, messages=st.session_state.messages)

        msg = response["message"]["content"]

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
