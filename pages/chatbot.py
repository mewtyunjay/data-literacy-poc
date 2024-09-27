import base64
import glob
import os

import streamlit as st
from openai import OpenAI
from st_clickable_images import clickable_images

import base_prompts as bp

st.set_page_config(
    page_title="Chatbot",
    page_icon=":robot:",
    # initial_sidebar_state="collapsed",
    )

# load images
evidence_paths = glob.glob("evidence/*.png")
evidence_images = []
for file in evidence_paths:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        evidence_images.append(f"data:image/jpeg;base64,{encoded}")

# load img_index selected from previous page
img_index = int(st.query_params.get("img_index", None))
chosen_evidence = evidence_images[img_index]
# st.image(chosen_evidence)

with st.sidebar:
    st.markdown("[View the source code](https://github.com/mewtyunjay/data-literacy-poc)")
    st.markdown("When you click on \"Save Evidence\", we create a summary of the conversation you had with the agent and then you can use this summary to create your data story")
    save_evidence = st.button("Save Evidence")

    st.markdown("When you click on \"Analyze Image\", the agent will provide you a simple analysis of the evidence you chose. This might be a good starting point!")
    analyze_image = st.button("Analyze Image")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# helpers to avoid wasting time
main_topic = "Social media usage by teenagers"
st.image(chosen_evidence)
# main_thesis = st.text_input(
#         "What are your initial thoughts on this image?"
# )
main_thesis = "I believe that teenagers should not use social media because it can polarize their views and they would lose their sense of nuance when discussing complex issues"

if "messages" not in st.session_state:
    welcome_message = f'You need to build an argument about \
    "{main_topic}" \
    and your starting point of view is "{main_thesis}". How do you think the image \
    you chose related to your main thesis?'
    # send instructions to agent
    st.session_state["messages"] = [
        {"role": "system", "content": bp.SYSTEM_INSTRUCTIONS}
    ]

    # provide topic and thesis as context to the agent
    st.session_state.messages.append({
        "role": "user",
        "content": f"We're discussing {main_topic} and my main thesis is \"{main_thesis}\""})
    st.chat_message("assistant").write(welcome_message)


if analyze_image:
    # add image as context
    messages = ([
        {"role": "system", "content": "You're a helpful assistant that will help analyzing this image"},
        {"role": "user", "content": [
            {"type": "text", "text": bp.IMAGE_PROMPT},
            {"type": "image_url", "image_url": {
                "url": f"{chosen_evidence}" },
            }
        ]}
    ])

    # st.chat_message("assistant").image(chosen_evidence)
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    msg = response.choices[0].message.content

    st.chat_message("assistant").write(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})

# display message history
# skip messages that were only providing context to the agent,
# display everything else
for idx, msg in enumerate(st.session_state.messages[3:]):
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages)
    msg = response.choices[0].message.content

    st.chat_message("assistant").write(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})


# download file
if save_evidence:
    st.write("Preparing summary...")
    # ask the chat to create a summary of the conversation
    prompt = "Create a two-paragraph summary of the conversation highlighting how the evidence is related to my argument and how that evolved during the conversation. Help me understand my position on the topic given the discussion. Keep language simple."

    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages[1::])
    summary = response.choices[0].message.content

    st.download_button("Download summary", summary, file_name=f"evidence_{[img_index]}.txt")
