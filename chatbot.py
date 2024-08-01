import glob
import os

import ollama
import streamlit as st

model = "llama3.1"
ollama.pull(model)

st.title("Data literacy chatbot")

@st.dialog("What topic would you like to discuss?")
def choose_main_topic():
    main_topic = st.radio(
        "",
        ["Social media usage by teenagers", "Gun violence"],
        index=None,
    )

    if st.button("Submit"):
        st.session_state.main_topic = main_topic
        st.rerun()


with st.sidebar:
    "[View the source code](https://github.com/mewtyunjay/data-literacy-poc)"

# main_topic = choose_main_topic()
main_thesis = ""

if "main_topic" not in st.session_state:
    choose_main_topic()
else:
    st.write(
        f"Let's start discussing {st.session_state.main_topic}! First, fill out the box below with your thesis and beliefs on the topic"
    )

    main_thesis = st.text_input(
        label="Thesis",
        placeholder="Example: I believe that teenagers should not use social media because it is hurtful",
    )

if main_thesis != "":
    # update sidebar with evidences
    # TODO: create specific evidences for specific discussion topics
    with st.sidebar:
        st.sidebar.title("Evidences")
        evidences = glob.glob("evidence/*.png")
        # pick_image = st.sidebar.radio(
        #         "Choose a evidence to start with",
        #         [e for e in evidences])
        st.sidebar.image(evidences)
    # st.text(f"You chose image {pick_image}")

    welcome_message = f'Ok, so you need to build an argument about "{main_topic}" \
    and your starting point of view is "{main_thesis}".\nOn your left \
    your should be able to see evidences for the topic you want to discuss, \
    choose one and let\'s analyze it together'

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": f"{welcome_message}"}
        ]


    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = ollama.chat(model=model, messages=st.session_state.messages)

        msg = response["message"]["content"]

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
