# UltraSteelChallenge/rfid/writer.py

import serial
import time
from app.config import SERIAL_PORT, BAUDRATE, TIMEOUT
from app.rfid.commands import WRITE_TAG_CMD_BASE, READ_SINGLE_CMD
from app.utils.hex_conv import txt2hex

def calc_checksum(cmd: list) -> int:
    return sum(cmd[1:]) & 0xFF

def format_data(text: str) -> str:
    text = text.strip()
    if len(text) > 24:
        print("⚠️ Data too long, trimming to 24 characters")
        text = text[:24]
    return text.ljust(24, "_")

def write_tag(data: str):
    formatted = format_data(data)
    hex_payload = txt2hex(formatted)
    data_bytes = list(bytes.fromhex(hex_payload))

    # Params: bank(1) + word ptr(1) + word count(1) + data(16 bytes = 8 words)
    param = [0x03, 0x00, 0x08] + data_bytes
    param_len = len(param)

    cmd = [0xAA, 0x00, 0x49, 0x00, param_len] + param
    checksum = sum(cmd[1:]) & 0xFF
    cmd.append(checksum)
    cmd.append(0xDD)

    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT) as ser:
        ser.write(READ_SINGLE_CMD)  # optional pre-select
        time.sleep(0.1)
        ser.flushInput()

        ser.write(bytes(cmd))
        time.sleep(0.2)
        response = ser.read(64)

        if not response or len(response) < 7:
            print("❌ No response")
            return False

        if response[0] != 0xAA or response[-1] != 0xDD:
            print("❌ Invalid frame")
            return False

        status_code = response[5]
        if status_code == 0x10:
            print("✅ Write successful")
            return True
        else:
            print(f"❌ Write failed, status code: {hex(status_code)}")
            return False
