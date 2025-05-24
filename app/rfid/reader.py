# UltraSteelChallenge/app/rfid/reader.py

# import re
# import serial
# import time
# from app.config import SERIAL_PORT, BAUDRATE, TIMEOUT
# from app.rfid.commands import READ_SINGLE_CMD
# from app.utils.hex_conv import hex2txt


# def extraer_epcs_limpios(data_bytes):
#     """Extract EPCs (12 bytes starting with E2) from the response bytes."""
#     epcs = []
#     data_hex = ' '.join(f'{b:02X}' for b in data_bytes)
#     matches = re.findall(r'(E2(?: [0-9A-F]{2}){11})', data_hex)
#     for m in matches:
#         epcs.append(m)
#     return epcs

# def read_tag(count=1):
#     """Continuously read RFID tags until `count` EPCs are read."""
#     ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
#     time.sleep(1)  # Wait for the serial connection to initialize
#     print(f"🧪 Starting to read {count} EPCs...")
#     read_count = 0

#     try:
#         while read_count < count:
#             ser.write(READ_SINGLE_CMD)
#             data = ser.read(128)
#             if data:
#                 epcs = extraer_epcs_limpios(data)
#                 for epc in epcs:
#                     read_count += 1
#                     print(f"[{read_count}] {epc}")
#                     print("📦 EPC:", hex2txt(epc))
#                     if read_count >= count:
#                         break
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("\n⛔ Test interrumpido.")
#     finally:
#         print("✅ Test completo.")
#         ser.close()

# if __name__ == "__main__":
#     while True:
#         data = read_tag()
#         if data:
#             print("📦 Data:", data)
#         time.sleep(1)

import serial
import time
import csv
import re
import requests
from datetime import datetime
from collections import defaultdict

# === CONFIG ===
PORT = '/dev/ttyUSB0'   # Update for Raspberry Pi or 'COM10' for Windows
BAUDRATE = 115200
PRODUCT_NAME = "Magic Wand XL"
LOT_NUMBER = "LOT2025A"
RECEIVED_BY = "JD"

# === GLOBALS ===
read_single_cmd = bytes([0xAA, 0x00, 0x22, 0x00, 0x00, 0x22, 0xDD])
epc_contador = defaultdict(int)
ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(1)  # Allow port to settle

# === UTILITIES ===
def extraer_epcs_limpios(data_bytes):
    """Extrae EPCs válidos de 96 bits que comienzan con E2."""
    epcs = []
    data_hex = ' '.join(f'{b:02X}' for b in data_bytes)
    matches = re.findall(r'(E2(?: [0-9A-F]{2}){11})', data_hex)
    for m in matches:
        epcs.append(m)
    return epcs


# === MAIN FUNCTIONS ===
def test_serial_read(count=5):
    print(f"🧪 Test: leyendo {count} EPCs...")
    read_count = 0
    try:
        while read_count < count:
            ser.write(read_single_cmd)
            data = ser.read(128)
            if data:
                epcs = extraer_epcs_limpios(data)
                for epc in epcs:
                    read_count += 1
                    print(f"[{read_count}] {epc}")
                    if read_count >= count:
                        break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ Test interrumpido.")
    finally:
        print("✅ Test completo.")
        ser.close()

# === ENTRY POINT ===
if __name__ == "__main__":
    test_serial_read()
