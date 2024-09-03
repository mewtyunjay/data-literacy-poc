import base64
import glob
import os

import streamlit as st
from openai import OpenAI
from st_clickable_images import clickable_images

import base_prompts as bp

def summarize_evidence_discussion(messages):
    summary_prompt = "Summarize the key points of the discussion about this evidence image in a concise manner."
    summary_messages = [
        {"role": "system", "content": "You are an AI assistant that summarizes discussions about evidence images."},
        *messages[1:],  # Exclude the system message
        {"role": "user", "content": summary_prompt}
    ]
    summary_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=summary_messages
    )
    return summary_response.choices[0].message.content

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
    tab1, tab2 = st.tabs(["Main Discussion", "Evidence"])

    with tab1:
        st.write(
            f"Let's start discussing {st.session_state.main_topic}! First, fill out the box below with your thesis and beliefs on the topic"
        )

        main_thesis = st.text_input(
            label="Thesis",
            placeholder="Example: I believe that teenagers should not use social media because it is hurtful",
        )

    if main_thesis != "":
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # Move evidence to sidebar
        with st.sidebar:
            st.sidebar.title("Evidences")
            evidence_paths = glob.glob("evidence/*.png")
            evidence_images = []
            for file in evidence_paths:
                with open(file, "rb") as image:
                    encoded = base64.b64encode(image.read()).decode()
                    evidence_images.append(f"data:image/jpeg;base64,{encoded}")

            clicked = clickable_images(
                evidence_images,
                titles=[f"Image #{str(i)}" for i in range(len(evidence_images))],
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "200px"},
            )

            st.session_state["clicked"] = clicked

        # Main discussion tab
        with tab1:
            if "messages" not in st.session_state:
                st.session_state["messages"] = [
                    {"role": "system", "content": bp.SYSTEM_INSTRUCTIONS}
                ]

                welcome_message = f'Ok, so you need to build an argument about \
                "{st.session_state.main_topic}" \
                and your starting point of view is "{main_thesis}".\nOn your left \
                you should be able to see evidences for the topic you want to discuss, \
                choose one and let\'s analyze it together'

                st.chat_message("assistant").write(welcome_message)

                st.session_state.messages.append({
                    "role": "user",
                    "content": f"We're discussing {st.session_state.main_topic} and my main thesis is \"{main_thesis}\""})

            # Display message history
            for idx, msg in enumerate(st.session_state.messages):
                if idx == 0:
                    continue
                st.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input():
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)
                response = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages)
                msg = response.choices[0].message.content

                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.chat_message("assistant").write(msg)

        # Evidence tab
        with tab2:
            if st.session_state["clicked"] > -1:
                st.image(evidence_paths[st.session_state["clicked"]])
                
                if "evidence_messages" not in st.session_state:
                    st.session_state["evidence_messages"] = [
                        {"role": "system", "content": "You are an AI assistant that helps analyze and discuss evidence images."}
                    ]

                # Display evidence chat history
                for msg in st.session_state["evidence_messages"][1:]:
                    st.chat_message(msg["role"]).write(msg["content"])

                evidence_prompt = st.chat_input("Discuss the evidence")
                if evidence_prompt:
                    st.session_state["evidence_messages"].append({"role": "user", "content": evidence_prompt})
                    st.chat_message("user").write(evidence_prompt)

                    evidence_response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            *st.session_state["evidence_messages"],
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": evidence_prompt},
                                    {"type": "image_url", "image_url": {"url": evidence_images[st.session_state["clicked"]]}}
                                ]
                            }
                        ]
                    )
                    evidence_msg = evidence_response.choices[0].message.content
                    st.session_state["evidence_messages"].append({"role": "assistant", "content": evidence_msg})
                    st.chat_message("assistant").write(evidence_msg)

                    # Summarize the evidence discussion and add it to the main bot's context
                    evidence_summary = summarize_evidence_discussion(st.session_state["evidence_messages"])
                    st.session_state["messages"].append({
                        "role": "system",
                        "content": f"Evidence discussion summary: {evidence_summary}"
                    })