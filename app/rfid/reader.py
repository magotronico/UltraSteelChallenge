import serial
import time
import re

def read_tags_loop(port='COM6', baudrate=115200, interval=1):
    def split_tags(data_string):
        data_string = data_string.strip()
        return re.findall(r'AA(?: [0-9A-F]{2})*? DD', data_string)

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
                        print("✅ EPC (HEX):", ' '.join(epc_data))
                        epc_ascii = ''.join(chr(int(b, 16)) for b in epc_data if 32 <= int(b, 16) <= 126)
                        print("✅ EPC (ASCII):", epc_ascii)
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

# Para ejecutar
read_tags_loop()
