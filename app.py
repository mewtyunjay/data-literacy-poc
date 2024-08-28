import streamlit as st
import os
from PIL import Image

# Define the list of topics
topics = ["Social media usage by teenagers", "Gun violence", "Climate change", "Online privacy"]

# Create a dropdown menu for topic selection
selected_topic = st.selectbox("Choose a topic to discuss:", topics)

# Store the selected topic in session state
if selected_topic:
    st.session_state.main_topic = selected_topic
    # Create a new "page" for the selected topic
    if st.button("Start Discussion"):
        st.session_state.page = "discussion"
        st.rerun()

# Check if we're on the discussion page
if st.session_state.get("page") == "discussion":
    st.header(st.session_state.main_topic)
    
    # Add a text input for the user's thesis
    main_thesis = st.text_input(
        label="Your Thesis",
        placeholder="Enter your main argument or belief about this topic"
    )
    
    if main_thesis:
        st.write(f"Your thesis: {main_thesis}")
        
        # Here you can add more components for discussion,
        # such as evidence display, counterarguments, etc.
        
        # Display evidence images in a carousel
        st.subheader("Evidence")
        
        # Get all image files from the 'evidence' folder
        evidence_folder = "evidence"
        image_files = [f for f in os.listdir(evidence_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        if image_files:
            # Create a selectbox for image selection
            selected_image = st.selectbox("Select evidence to view:", image_files)
            
            # Display the selected image
            image_path = os.path.join(evidence_folder, selected_image)
            image = Image.open(image_path)
            st.image(image, caption=selected_image, use_column_width=False, width=800)  # Reduced size
            
            # Add navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Previous"):
                    current_index = image_files.index(selected_image)
                    prev_index = (current_index - 1) % len(image_files)
                    st.session_state.selected_image = image_files[prev_index]
                    st.rerun()
            with col2:
                if st.button("Next"):
                    current_index = image_files.index(selected_image)
                    next_index = (current_index + 1) % len(image_files)
                    st.session_state.selected_image = image_files[next_index]
                    st.rerun()
        else:
            st.write("No evidence images found in the 'evidence' folder.")

