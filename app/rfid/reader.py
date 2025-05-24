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



def read_tag(count=5):
    """Continuously read RFID tags until `count` EPCs are read."""
    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT) as ser:
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
                        print(f"[{read_count}] EPC: {epc}")
                        if epc:
                            text = hex2txt(epc.replace(' ', ''))
                            print(f"📦 EPC Text: {text}")
                        else:
                            print("⚠️ Empty EPC received")
                        if read_count >= count:
                            break
                else:
                    print("⚠️ No data received")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⛔ Reading interrupted by user.")
        finally:
            print("✅ Reading complete.")
if __name__ == "__main__":
    while True:
        data = read_tag()
        if data:
            print("📦 Data:", data)
        time.sleep(1)
