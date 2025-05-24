# UltraSteelChallenge/rfid/writer.py

import serial
import time
from app.config import SERIAL_PORT, BAUDRATE, TIMEOUT
from app.rfid.commands import WRITE_TAG_CMD_BASE
from app.utils.hex_conv import txt2hex

def calc_checksum(cmd: list) -> int:
    return sum(cmd[1:]) & 0xFF

def format_data(text: str) -> str:
    text = text.strip()
    if len(text) > 24:
        print("⚠️ Data too long, trimming to 24 characters")
        text = text[:24]
    return text.ljust(24, "_")  # Pad with underscores for consistency

def write_tag(data: str):
    formatted = format_data(data)
    hex_payload = txt2hex(formatted)
    data_bytes = list(bytes.fromhex(hex_payload))

    full_cmd = WRITE_TAG_CMD_BASE + data_bytes
    checksum = calc_checksum(full_cmd)
    full_cmd.append(checksum)
    full_cmd.append(0xDD)

    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT) as ser:
        ser.write(bytes(full_cmd))
        time.sleep(0.2)
        response = ser.read(64)

        if not response or response[0] != 0xAA or response[-1] != 0xDD:
            print("❌ Write failed or invalid response")
            return False

        status_code = response[5]
        if status_code == 0x10:
            print("✅ Write successful")
            return True
        else:
            print(f"⚠️ Write failed, status code: {status_code}")
            return False
