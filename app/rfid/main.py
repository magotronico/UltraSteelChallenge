import serial
import time
import re
from app.config import SERIAL_PORT, BAUDRATE

SERIAL_PORT = 'COM6'
BAUDRATE = 115200

def split_tags(data_string):
    data_string = data_string.strip()
    return re.findall(r'AA(?: [0-9A-F]{2})*? DD', data_string)

def read_tags_loop(port=SERIAL_PORT, baudrate=BAUDRATE, interval=1):
    read_cmd = bytes([
        0xAA, 0x00, 0x22, 0x00, 0x00,
        0x22, 0xDD
    ])

    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print("📡 Escaneando etiquetas RFID. Presiona Ctrl+C para detener.\n")
        while True:
            ser.write(read_cmd)
            response = ser.read(64)

            if response:
                response_str = ' '.join(f'{b:02X}' for b in response)
                tags = split_tags(response_str)
                print(f"\n🔍 Etiquetas encontradas: {len(tags)}")

                for tag in tags:
                    tag_parts = tag.split(" ")
                    try:
                        header_index = tag_parts.index('AA')
                        epc_len = int(tag_parts[header_index + 2], 16) // 2
                        epc_data = tag_parts[header_index + 8:header_index + 3 + epc_len]
                        epc_ascii = ''.join(chr(int(b, 16)) for b in epc_data if 32 <= int(b, 16) <= 126)
                        print("✅ EPC (HEX):", ' '.join(epc_data), "\nEPC (ASCII):", epc_ascii)
                    except Exception as e:
                        print("⚠ No se pudo extraer el EPC:", e)
            else:
                print("\n❌ No se detectó respuesta del lector.")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n🛑 Lectura detenida por el usuario.")
    except Exception as err:
        print("⚠ Error al comunicar con el puerto serial:", err)
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

def write_epc_data(data_str):
    if len(data_str) > 12:
        raise ValueError("❌ Máximo 12 caracteres (12 bytes / 6 palabras) permitido.")

    data_bytes = list(data_str.encode('ascii'))
    data_bytes += [0x00] * (12 - len(data_bytes))

    header = [0xAA]
    frame_type = [0x00]
    command = [0x49]
    access_password = [0x00, 0x00, 0x00, 0x00]
    membank = [0x01]  # EPC memory
    word_pointer = [0x00, 0x02]
    word_count = [0x00, 0x06]
    parameters = access_password + membank + word_pointer + word_count + data_bytes
    param_len = [len(parameters) >> 8, len(parameters) & 0xFF]

    body = frame_type + command + param_len + parameters
    checksum = [sum(body) & 0xFF]
    end_byte = [0xDD]
    frame = header + body + checksum + end_byte

    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    time.sleep(1)
    ser.write(bytes(frame))
    time.sleep(1)
    response = ser.read(64)
    ser.close()

    print("\n📤 Enviado:")
    print(' '.join(f'{b:02X}' for b in frame))

    if response:
        print("📥 Respuesta recibida:")
        response2 = [f'{b:02X}' for b in response]
        print(' '.join(response2))
        if response2[2] == '49':
            print("✅ Escritura exitosa.")
        elif response2[2] == 'FF':
            print(f"❌ Error del lector. Código: {response[5]:02X}")
        else:
            print("⚠ Respuesta inesperada.")
    else:
        print("❌ No hubo respuesta del lector.")

def main():
    while True:
        print("=== LECTOR / ESCRITOR RFID ===")
        print("1. Leer etiquetas")
        print("2. Escribir EPC")
        option = input("Selecciona una opción (1/2): ").strip()

        if option == '1':
            read_tags_loop()
        elif option == '2':
            epc_data = input("Ingresa el texto a escribir (máx 12 caracteres): ").strip()
            write_epc_data(epc_data)
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    main()
