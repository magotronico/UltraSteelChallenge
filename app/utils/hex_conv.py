# UltraSteelChallenge/app/utils/hex_conv.py

def txt2hex(text: str) -> str:
    # Convierte texto ASCII a string hex sin espacios, ej: "hello" -> "68656C6C6F"
    try:
        return ''.join(f'{ord(c):02X}' for c in text)
    except Exception:
        return ""

def hex2txt(hex_str: str) -> str:
    # Convierte string hex sin espacios a ASCII, ej: "68656C6C6F" -> "hello"
    try:
        bytes_obj = bytes.fromhex(hex_str)
        return bytes_obj.decode('ascii')
    except Exception:
        return ""
