import base64
import glob
import os

import streamlit as st
from st_clickable_images import clickable_images
from streamlit_extras.switch_page_button import switch_page

# from chatbot import discuss_evidence

st.title(":bookmark_tabs: Evidence Selector")
st.text("Choose one image from the list below")

# define our two columns
image_list, image_selection = st.columns(2, gap="large")

img = st.query_params.get("img", None)
img_index = st.query_params.get("img_index", None)
clicked = -1

with image_list:
    # initialize evidence images
    evidence_paths = glob.glob("evidence/*.png")
    evidence_images = []
    for file in evidence_paths:
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            evidence_images.append(f"data:image/jpeg;base64,{encoded}")

    if img is None:
        clicked = clickable_images(
            evidence_images,
            titles=[f"Image #{str(i)}" for i in range(5)],
            # div_style={"display": "flex", "flex-wrap": "wrap"},
            img_style={"height": "400px"},
        )

        # wtf
        clicked = clicked

with image_selection:
    if img is not None and img_index is not None:
        img_index = int(img_index)
    elif img is None and clicked > -1:
        f"## {clicked} is a great choice! "
        st.image(evidence_images[clicked], caption=f"{clicked}!")
        st.link_button(
            url=f"./chatbot?img_index={clicked}",
            label=f"Discuss image {clicked}",
            use_container_width=True
        )
