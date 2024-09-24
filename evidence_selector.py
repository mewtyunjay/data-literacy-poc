import base64
import glob
import os

import streamlit as st
from st_clickable_images import clickable_images

st.set_page_config(
    page_title="Evidence Selector",
    page_icon=":bookmark_tabs:",
    layout="wide",
    initial_sidebar_state="collapsed",
    )


st.markdown("# Choose one image from the list below")

# define our two columns and make sure image_list is 2x the size of
# image_selection
image_list, image_selection = st.columns((2,1), gap="large")

with image_list:
    img_container = image_list.container(height=1000)
    with img_container:
        evidence_paths = glob.glob("evidence/*.png")
        evidence_images = []
        for file in evidence_paths:
            with open(file, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
                evidence_images.append(f"data:image/jpeg;base64,{encoded}")

        clicked = clickable_images(
            evidence_images,
            titles=[f"{os.path.basename(i)}" for i in evidence_paths],
            # div_style={"display": "flex", "flex-wrap": "wrap"},
            # img_style={"heigth": "100px"},
        )

with image_selection:
    if clicked > -1:
        st.image(evidence_images[clicked],
                caption=f"{os.path.basename(evidence_paths[clicked])}")
        st.link_button(
            url=f"./chatbot?img_index={clicked}",
            label="Discuss this image",
            use_container_width=True
        )
