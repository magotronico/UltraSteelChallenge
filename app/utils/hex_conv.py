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

if __name__ == "__main__":
    # Pruebas rápidas
    sample_text = "hello"
    hex_output = txt2hex(sample_text)
    print(f"Texto: {sample_text} -> Hex: {hex_output}")

    sample_hex = "68656C6C6F"
    text_output = hex2txt(sample_hex)
    print(f"Hex: {sample_hex} -> Texto: {text_output}")