# UltraSteelChallenge/app/utils/hex_conv.py

def txt2hex(text: str) -> str:
    return text.encode('utf-8').hex()

def hex2txt(hex_str: str) -> str:
    """
    Convert a hex string (e.g. '414243') to ASCII text ('ABC').
    Removes any padding underscores or nulls.
    """
    try:
        bytes_data = bytes.fromhex(hex_str)
        text = bytes_data.decode('ascii').rstrip('\x00').rstrip('_')
        return text
    except Exception as e:
        print(f"Error decoding hex to text: {e}")
        return ""