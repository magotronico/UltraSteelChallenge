# UltraSteelChallenge/app/utils/hex_conv.py

def txt2hex(text: str) -> str:
    return text.encode('utf-8').hex()

def hex2txt(hex_str: str) -> str:
    return bytes.fromhex(hex_str).decode('utf-8')