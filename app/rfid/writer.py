# UltraSteelChallenge/app/rfid/writer.py

# Librearies
import serial
import time
from app.config import SERIAL_PORT, BAUDRATE


# Function to write data to RFID tag
def write_tag(data_str: str) -> None:
    """
    Write a string to an RFID tag.

    This function encodes a text string into ASCII, formats it into a write 
    command frame according to the RFID protocol, and sends it to the RFID writer 
    via the configured serial port.

    Parameters
    ----------
    data_str : str
        The text to write to the RFID tag (maximum of 12 characters).

    Raises
    ------
    ValueError
        If the input string exceeds 12 characters.
    """

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


# Main function to run the writer
if __name__ == "__main__":
    while True:
        try:
            sample_data = input("📝 Ingrese el texto a escribir en la etiqueta (máx 12 caracteres): ")
            write_tag(sample_data)
        except ValueError as ve:
            print(ve)
        except KeyboardInterrupt:
            print("\n🛑 Escritura detenida por el usuario.")
            break
        except Exception as e:
            print(f"⚠ Error al escribir la etiqueta: {e}")