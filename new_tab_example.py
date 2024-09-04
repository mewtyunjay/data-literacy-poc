import base64
import glob
import os

import streamlit as st
from st_clickable_images import clickable_images

from chatbot import discuss_evidence

img = st.query_params.get("img", None)
img_index = st.query_params.get("img_index", None)
clicked = -1

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
        div_style={"display": "flex", "flex-wrap": "wrap"},
        img_style={"height": "400px"},
    )

    st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

    clicked = clicked
    # print("img = ", img)
    # print("clicked = ", clicked)

if img is not None and img_index is not None:
    # st.text(f"we clicked image {img_index}")
    img_index = int(img_index)
    # st.image(evidence_images[img_index])
    # TODO: discuss evidence func
    discuss_evidence(evidence_images[img_index])
elif img is None and clicked > -1:
    f"## {clicked} is a great choice! "
    st.image(evidence_images[clicked],
            caption=f"{clicked}!")
    st.link_button(
        "See more!",
        url=f"http://localhost:8501/?img={clicked}&img_index={clicked}",
        use_container_width=True
    )
