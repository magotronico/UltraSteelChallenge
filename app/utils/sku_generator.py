def generate_sku(name: str) -> str:
    return ''.join(word[0].upper() for word in name.split())[:6]
