import streamlit as st
from PIL import Image
import cv2
import numpy as np
import os
from sketchpy import canvas
import matplotlib.pyplot as plt

st.title("🖼️ Image to Sketch Converter")
st.write("Apni image upload karein aur sketch banayein!")

# File uploader
uploaded_file = st.file_uploader("Apni image upload karein", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Image save karein
    with open("temp_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("Image successfully uploaded!")
    
    # Display original image
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(uploaded_file, use_column_width=True)
    
    with col2:
        st.subheader("Sketch")
        
        # Sketch banayein
        try:
            # Sketchpy use karte hain
            sketch = canvas.trace_from_image("temp_image.png", save=False, scale=0.5)
            
            # Temporary file for sketch
            sketch_output = "sketch_output.png"
            # Yahan aap ko thora code modify karna hoga sketch save karne ke liye
            
            st.info("Sketch ban raha hai...")
            
            # Alternative method agar sketchpy kaam na kare
            img = cv2.imread("temp_image.png")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            inverted = 255 - gray
            blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
            inverted_blurred = 255 - blurred
            pencil_sketch = cv2.divide(gray, inverted_blurred, scale=256.0)
            
            st.image(pencil_sketch, use_column_width=True, clamp=True)
            
            # Download button
            cv2.imwrite("sketch_result.png", pencil_sketch)
            with open("sketch_result.png", "rb") as file:
                btn = st.download_button(
                    label="Sketch Download Karein",
                    data=file,
                    file_name="my_sketch.png",
                    mime="image/png"
                )
                
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Alternative method use kar raha hoon...")

# Clean up
if os.path.exists("temp_image.png"):
    os.remove("temp_image.png")
if os.path.exists("sketch_result.png"):
    os.remove("sketch_result.png")
