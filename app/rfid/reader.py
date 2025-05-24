# UltraSteelChallenge/app/rfid/reader.py

import serial
import time
from app.config import SERIAL_PORT, BAUDRATE, TIMEOUT
from app.rfid.commands import READ_SINGLE_CMD
from app.utils.hex_conv import hex2txt


def build_read_user_cmd(word_count=12):
    cmd = [0xAA, 0x00, 0x39, 0x00, 0x03, 0x03, 0x00, word_count]
    checksum = sum(cmd[1:]) & 0xFF
    return bytes(cmd + [checksum, 0xDD])



def read_tag():
    read_cmd = build_read_user_cmd(12)
    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT) as ser:
        # Pre-select tag
        ser.write(READ_SINGLE_CMD)
        time.sleep(0.1)
        _ = ser.read(128)
        ser.flushInput()

        # Read User memory
        ser.write(read_cmd)
        time.sleep(0.3)
        response = ser.read(64)

        if not response or len(response) < 10:
            print("❌ No or too short response")
            return None

        if response[0] != 0xAA or response[-1] != 0xDD:
            print("❌ Invalid frame")
            return None

        status = response[5]
        if status != 0x10:
            print(f"❌ Read failed, status {hex(status)}")
            return None

        data_bytes = response[6:-2]  # Payload bytes
        hex_str = ''.join(f'{b:02X}' for b in data_bytes)
        text = hex2txt(hex_str)
        print("✅ Read data:", text)
        return text

if __name__ == "__main__":
    while True:
        data = read_tag()
        if data:
            print("📦 Data:", data)
        time.sleep(1)
