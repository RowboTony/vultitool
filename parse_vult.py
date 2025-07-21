import base64
import sys

def parse_vult(file_path):
    try:
        with open(file_path, 'r') as file:
            encoded_content = file.read().strip()
            decoded_content = base64.b64decode(encoded_content).decode('utf-8')
            print("Decoded Content:\n", decoded_content)
    except Exception as e:
        print(f"Error reading or decoding file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_vult.py <path_to_vult_file>")
    else:
        parse_vult(sys.argv[1])

