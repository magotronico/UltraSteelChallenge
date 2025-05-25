import serial
import time

PORT = 'COM6'
BAUDRATE = 115200

def calculate_checksum(frame_bytes):
    return sum(frame_bytes) & 0xFF

def write_epc_data(data_str):
    if len(data_str) > 12:
        raise ValueError("❌ Maximum 12 characters (12 bytes / 6 words) allowed.")

    # Convert string to bytes and pad to 12 bytes if needed
    data_bytes = list(data_str.encode('ascii'))
    data_bytes += [0x00] * (12 - len(data_bytes))

    # Build command fields
    header = [0xAA]
    frame_type = [0x00]
    command = [0x49]
    access_password = [0x00, 0x00, 0x00, 0x00]
    membank = [0x01]  # EPC memory
    word_pointer = [0x00, 0x02]
    word_count = [0x00, 0x06]  # 6 words = 12 bytes
    parameters = access_password + membank + word_pointer + word_count + data_bytes
    param_len = [len(parameters) >> 8, len(parameters) & 0xFF]

    # Combine full frame
    body = frame_type + command + param_len + parameters
    checksum = [calculate_checksum(body)]
    end_byte = [0xDD]
    frame = header + body + checksum + end_byte

    # Send frame to reader
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(1)
    ser.write(bytes(frame))
    time.sleep(1)  # Esperar un poco para que el lector procese
    response = ser.read(64)
    ser.close()

    print("\n📤 Enviado:")
    print(' '.join(f'{b:02X}' for b in frame))

    if response:
        print("📥 Respuesta recibida:")
        response2 = [f'{b:02X}' for b in response]
        print(' '.join(f'{b:02X}' for b in response))
        if response2[2] == '49':
            print("✅ Escritura exitosa.")
        elif response[2] == 'FF':
            print(f"❌ Error del lector. Código: {response[5]:02X}")
        else:
            print("⚠ Respuesta inesperada.")
    else:
        print("❌ No hubo respuesta del lector.")

# ▶ Example usage
write_epc_data("a")
