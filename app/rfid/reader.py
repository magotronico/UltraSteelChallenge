# UltraSteelChallenge/app/rfid/reader.py

import serial
import time
import re
from app.config import SERIAL_PORT, BAUDRATE, TIMEOUT
from app.rfid.commands import READ_SINGLE_CMD

def extraer_epcs_limpios(data_bytes):
    """Extract EPCs (12 bytes starting with E2) from the response."""
    epcs = []
    data_hex = ' '.join(f'{b:02X}' for b in data_bytes)
    # Extract 12-byte EPCs starting with E2
    matches = re.findall(r'(E2(?: [0-9A-F]{2}){11})', data_hex)
    for m in matches:
        epcs.append(m)
    return epcs

def read_tag():
    """
    Read EPCs from an RFID tag using READ_SINGLE_CMD.
    Returns a list of EPCs found in the response, or None if no EPCs are found.
    """
    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT) as ser:
        ser.write(READ_SINGLE_CMD)
        time.sleep(0.1)
        response = ser.read(128)

        if not response:
            print("⚠️ No response")
            return None

        epcs = extraer_epcs_limpios(response)
        if not epcs:
            print("⚠️ No EPCs found in response")
            return None

        return epcs