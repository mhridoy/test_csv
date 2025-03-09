import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import numpy as np
from pyzbar import pyzbar
import base64
from datetime import datetime

# Function to decode TLV encoded QR code data
def decode_tlv(encoded_data):
    index = 0
    decoded_data = {}
    while index < len(encoded_data):
        tag = encoded_data[index]
        length = encoded_data[index + 1]
        value = encoded_data[index + 2: index + 2 + length].decode('utf-8')
        if tag == 1:
            decoded_data['Seller Name'] = value
        elif tag == 2:
            decoded_data['VAT Registration Number'] = value
        elif tag == 3:
            decoded_data['Invoice Timestamp'] = value
        elif tag == 4:
            decoded_data['Invoice Total (with VAT)'] = value
        elif tag == 5:
            decoded_data['VAT Total'] = value
        index += 2 + length
    return decoded_data

# Video processor class for real-time QR code detection
class QRCodeProcessor(VideoProcessorBase):
    def __init__(self):
        self.decoded_info = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        decoded_objects = pyzbar.decode(img)
        for obj in decoded_objects:
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points
            n = len(hull)
            for j in range(0, n):
                cv2.line(img, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)

            qr_data = obj.data
            try:
                decoded_data = base64.b64decode(qr_data)
                self.decoded_info = decode_tlv(decoded_data)
            except Exception as e:
                self.decoded_info = {"Error": str(e)}

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Streamlit application layout
st.title("KSA E-Invoice QR Code Scanner with Live Camera")
st.write("Scan a KSA E-Invoice QR code using your webcam.")

# Initialize the QR code processor
ctx = webrtc_streamer(key="qr-code-scanner", video_processor_factory=QRCodeProcessor)

# Display decoded information
if ctx.video_processor:
    if ctx.video_processor.decoded_info:
        st.subheader("Decoded QR Code Data:")
        for key, value in ctx.video_processor.decoded_info.items():
            if key == 'Invoice Timestamp':
                try:
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')
                except ValueError:
                    pass
            st.write(f"**{key}**: {value}")
