import base64
import glob
import os

import streamlit as st
from openai import OpenAI
from st_clickable_images import clickable_images
import chromadb
from chromadb.config import Settings

chroma_client = chromadb.Client(Settings(persist_directory="./chroma_db"))
collection = chroma_client.get_collection(name="image_vectors")

def find_relevant_images(user_story, n=3):
    results = collection.query(
        query_texts=[user_story],
        n_results=n
    )
    return results['ids']

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
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    # update sidebar with evidences
    # TODO: create specific evidences for specific discussion topics
    with st.sidebar:
        st.sidebar.title("Evidences")
        evidence_paths = glob.glob("evidence/*.png")
        evidence_images = []
        for file in evidence_paths:
            with open(file, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
                evidence_images.append(f"data:image/jpeg;base64,{encoded}")

        # st.sidebar.image(clickable_images(evidence_images))
        clicked = clickable_images(
            evidence_images,
            titles=[f"Image #{str(i)}" for i in range(len(evidence_images))],
            div_style={"display": "flex", "justify-content": "center",
                "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "200px"},
        )

        st.session_state["clicked"] = clicked

    welcome_message = f'Ok, so you need to build an argument about \
    "{st.session_state.main_topic}" \
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
        text_content = {"type": "text", "text": prompt}
        content = [text_content]
        
        # Find relevant images based on user input
        relevant_image_ids = find_relevant_images(prompt)
        
        # Update sidebar with relevant images
        with st.sidebar:
            st.sidebar.title("Relevant Evidences")
            relevant_evidence_paths = [f"evidence/{img_id}.png" for img_id in relevant_image_ids]
            relevant_evidence_images = []
            for file in relevant_evidence_paths:
                with open(file, "rb") as image:
                    encoded = base64.b64encode(image.read()).decode()
                    relevant_evidence_images.append(f"data:image/jpeg;base64,{encoded}")
            
            clicked = clickable_images(
                relevant_evidence_images,
                titles=[f"Image #{str(i)}" for i in range(len(relevant_evidence_images))],
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "200px"},
            )

        st.session_state["clicked"] = clicked

        if st.session_state.clicked > -1:
            st.image(evidence_paths[st.session_state.clicked])

            st.session_state.clicked_image = evidence_images[st.session_state.clicked]
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{evidence_images[st.session_state.clicked]}"
                    }
                })

            # reset clicked image
            st.session_state.clicked = -1

        st.session_state.messages.append({"role": "user", "content": content})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages)
        msg = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)