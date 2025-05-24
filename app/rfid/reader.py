# UltraSteelChallenge/app/rfid/reader.py

import serial
import time
from app.config import SERIAL_PORT, BAUDRATE, TIMEOUT
from app.rfid.commands import READ_SINGLE_CMD, READ_TAG_CMD
from app.utils.hex_conv import hex2txt

def read_tag():
    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT) as ser:
        # Inventory - ensure tag is present
        ser.write(READ_SINGLE_CMD)
        time.sleep(0.1)
        ser.flushInput()

        # Read User memory (24 bytes)
        ser.write(READ_TAG_CMD)
        time.sleep(0.2)
        response = ser.read(64)

        if not response or len(response) < 10:
            print("⚠️ No valid response")
            return None

        if response[0] != 0xAA or response[-1] != 0xDD:
            print("❌ Invalid frame")
            return None

        payload = response[7:-2]  # Skip header + command metadata + checksum
        if not payload:
            print("⚠️ No data in tag")
            return None

        try:
            return hex2txt(payload.hex())
        except Exception as e:
            print(f"❌ Failed to decode hex: {e}")
            return None

