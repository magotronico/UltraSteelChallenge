import serial
import time

PORT = 'COM6'
BAUDRATE = 115200

# Comando de lectura EPC (puede variar según el lector)
read_epc_cmd = bytes([
    0xAA, 0x00, 0x22, 0x00, 0x00,  # Ejemplo de comando genérico para leer EPC
    0x22, 0xDD                     # Comando puede necesitar ajuste si usas otro protocolo
])

# Abrir puerto
ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(1)
ser.write(read_epc_cmd)

# Leer respuesta
response = ser.read(64)
ser.close()

if response:
    print("\n📥 Respuesta recibida:")
    print(' '.join(f'{b:02X}' for b in response))

    try:
        # Buscar el encabezado del paquete
        header_index = response.index(0xAA)
        epc_len = response[header_index + 2] // 2
        epc_data = response[header_index + 8:header_index + 3 + epc_len]
        print(epc_len, header_index, epc_data)
        
        # Mostrar EPC
        print("✅ EPC (HEX):", ' '.join(f'{b:02X}' for b in epc_data))
        try:
            epc_ascii = ''.join(chr(b) for b in epc_data if 32 <= b <= 126)
            print("✅ EPC (ASCII):", epc_ascii)
        except:
            pass
    except Exception as e:
        print("⚠ No se pudo extraer el EPC:", e)
else:
    print("❌ No hubo respuesta del lector.")