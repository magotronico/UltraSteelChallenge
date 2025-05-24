# UltraSteelChallenge/app/rfid/reader.py

import re
import serial
import time
from app.config import SERIAL_PORT, BAUDRATE, TIMEOUT
from app.rfid.commands import READ_SINGLE_CMD
from app.utils.hex_conv import hex2txt


def extraer_epcs_limpios(data_bytes):
    """Extract EPCs (12 bytes starting with E2) from the response bytes."""
    epcs = []
    data_hex = ' '.join(f'{b:02X}' for b in data_bytes)
    matches = re.findall(r'(E2(?: [0-9A-F]{2}){11})', data_hex)
    for m in matches:
        epcs.append(m)
    return epcs



def read_tag(count=1):
    """Continuously read RFID tags until `count` EPCs are read."""
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    time.sleep(1)  # Wait for the serial connection to initialize
    print(f"🧪 Starting to read {count} EPCs...")
    read_count = 0

    try:
        while read_count < count:
            ser.write(READ_SINGLE_CMD)
            data = ser.read(128)
            if data:
                epcs = extraer_epcs_limpios(data)
                for epc in epcs:
                    read_count += 1
                    print(f"[{read_count}] {epc}")
                    print("📦 EPC:", hex2txt(epc))
                    if read_count >= count:
                        break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ Test interrumpido.")
    finally:
        print("✅ Test completo.")
        ser.close()

if __name__ == "__main__":
    while True:
        data = read_tag()
        if data:
            print("📦 Data:", data)
        time.sleep(1)
