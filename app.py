import streamlit as st
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np

st.title("QR Code Scanner")

# Function to decode QR codes
def decode_qr(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        st.write("Type:", obj.type)
        st.write("Data:", obj.data.decode("utf-8"))
        # Draw a rectangle around the QR code
        pts = np.array(obj.polygon, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
    return image

# Capture image from user
uploaded_file = st.file_uploader("Upload an image containing a QR code", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Decode the QR code
    decoded_image = decode_qr(image)

    # Display the image with QR code highlighted
    st.image(decoded_image, caption='Processed Image', use_column_width=True)
