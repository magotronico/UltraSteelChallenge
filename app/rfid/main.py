import serial
import time

PORT = 'COM6'
BAUDRATE = 115200

def calculate_checksum(frame_bytes):
    return sum(frame_bytes) & 0xFF

def write_epc_data(data_str):
    if len(data_str) > 12:
        raise ValueError("❌ Máximo 12 caracteres permitidos (12 bytes / 6 palabras).")

    # Convertir a bytes y rellenar hasta 12
    data_bytes = list(data_str.encode('ascii'))
    data_bytes += [0x00] * (12 - len(data_bytes))

    access_password = [0x00, 0x00, 0x00, 0x00]
    membank = [0x01]
    word_pointer = [0x00, 0x02]
    word_count = [0x00, 0x06]
    parameters = access_password + membank + word_pointer + word_count + data_bytes
    param_len = [len(parameters) >> 8, len(parameters) & 0xFF]

    frame_type = [0x00]
    command = [0x49]
    header = [0xAA]
    body = frame_type + command + param_len + parameters
    checksum = [calculate_checksum(body)]
    end_byte = [0xDD]
    frame = header + body + checksum + end_byte

    # Enviar comando
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(1)
    ser.write(bytes(frame))
    time.sleep(1)
    response = ser.read(64)
    ser.close()

    print("\n📤 Enviado:")
    print(' '.join(f'{b:02X}' for b in frame))

    if response:
        print("📥 Respuesta recibida:")
        print(' '.join(f'{b:02X}' for b in response))
        if response[2] == 0x49:
            print("✅ Escritura exitosa.")
        elif response[2] == 0xFF:
            print(f"❌ Error del lector. Código: {response[5]:02X}")
        else:
            print("⚠ Respuesta inesperada.")
    else:
        print("❌ No hubo respuesta del lector.")

def read_epc():
    read_epc_cmd = bytes([
        0xAA, 0x00, 0x22, 0x00, 0x00,
        0x22, 0xDD
    ])

    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(1)
    ser.write(read_epc_cmd)
    response = ser.read(64)
    ser.close()

    if response:
        print("\n📥 Respuesta recibida:")
        print(' '.join(f'{b:02X}' for b in response))
        try:
            header_index = response.index(0xAA)
            epc_len = response[header_index + 2] // 2
            epc_data = response[header_index + 8:header_index + 3 + epc_len]
            print("✅ EPC (HEX):", ' '.join(f'{b:02X}' for b in epc_data))
            epc_ascii = ''.join(chr(b) for b in epc_data if 32 <= b <= 126)
            print("✅ EPC (ASCII):", epc_ascii)
        except Exception as e:
            print("⚠ No se pudo extraer el EPC:", e)
    else:
        print("❌ No hubo respuesta del lector.")

def menu():
    while True:
        print("\n===== MENÚ RFID =====")
        print("1. Leer etiqueta")
        print("2. Escribir etiqueta")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            read_epc()
        elif opcion == "2":
            texto = input("Ingresa texto (máx 12 caracteres): ")
            try:
                write_epc_data(texto)
            except ValueError as e:
                print(e)
        elif opcion == "3":
            print("👋 Saliendo del programa.")
            break
        else:
            print("❌ Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    menu()
