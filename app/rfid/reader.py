# UltraSteelChallenge/app/rfid/reader.py

import serial
import time
from app.config import SERIAL_PORT, BAUDRATE, TIMEOUT
from app.rfid.commands import READ_SINGLE_CMD
from app.utils.hex_conv import hex2txt

def build_read_user_cmd(word_count=8):
    """
    Builds a command to read from USER memory bank (bank 0x03).
    Defaults to reading 8 words (16 bytes).
    """
    bank = 0x03
    start_addr = 0x00
    cmd_header = [0xAA, 0x00, 0x39, 0x00, 0x03, bank, start_addr, word_count]
    checksum = sum(cmd_header[1:]) & 0xFF
    return bytes(cmd_header + [checksum, 0xDD])

def read_tag_data():
    read_cmd = build_read_user_cmd(word_count=8)  # Read 8 words = 16 bytes

    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT) as ser:
        # First select a tag
        ser.write(READ_SINGLE_CMD)
        time.sleep(0.1)
        ser.flushInput()

        # Then read data from selected tag
        ser.write(read_cmd)
        time.sleep(0.2)
        response = ser.read(64)

        if not response or len(response) < 10:
            print("⚠️ No response or too short")
            return None

        if response[0] != 0xAA or response[-1] != 0xDD:
            print("⚠️ Invalid response framing")
            return None

        # Usually: response[6:] holds the payload
        # Example: [AA, 00, 39, 00, LEN, STATUS, DATA..., CHECKSUM, DD]
        status = response[5]
        if status != 0x10:
            print(f"❌ Read failed, status code: {hex(status)}")
            return None

        data_payload = response[6:-2]  # Exclude status, checksum, and footer
        if not data_payload:
            print("⚠️ No data payload")
            return None

        # Convert to string
        hex_string = ''.join(f'{b:02X}' for b in data_payload)
        return hex2txt(hex_string)

if __name__ == "__main__":
    text = read_tag_data()
    if text:
        print("📦 Tag Data:", text)
