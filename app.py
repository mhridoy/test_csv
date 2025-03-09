import base64
import struct

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
