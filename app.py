import streamlit as st
import numpy as np
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import base64
import struct

st.title("QR Code Scanner")

def zatca_qr_decoder(encoded_data):
    """Decodes ZATCA (Saudi VAT Invoice) QR Code."""
    tag_types = {1: "Seller", 2: "VAT Number", 3: "Timestamp", 4: "Total", 5: "VAT"}
    
    try:
        decoded_bytes = base64.b64decode(encoded_data)
        index = 0
        output = {}

        while index < len(decoded_bytes):
            tag = decoded_bytes[index]
            length = decoded_bytes[index + 1]
            value = decoded_bytes[index + 2 : index + 2 + length].decode("utf-8")

            output[tag_types.get(tag, f"Unknown ({tag})")] = value
            index += 2 + length

        return output
    except Exception as e:
        return f"Decoding Error: {str(e)}"
def decode_qr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    decoded_objects = decode(gray)

    if decoded_objects:
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")  # Extract QR code text
            if qr_data.startswith("AQ"):  # ZATCA QR codes are base64-encoded
                decoded_zatca = zatca_qr_decoder(qr_data)
                st.json(decoded_zatca)
            else:
                st.success(f"QR Code Data: {qr_data}")
        return image
    else:
        st.error("No QR code detected.")
        return image

# Upload image
uploaded_file = st.file_uploader("Upload an image containing a QR code", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Convert file to OpenCV format
    image = np.array(Image.open(uploaded_file))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Decode QR Code
    processed_image = decode_qr(image)

    # Display the image
    st.image(processed_image, caption="Processed Image", use_container_width=True)
