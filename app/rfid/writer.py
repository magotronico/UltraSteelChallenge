# UltraSteelChallenge/rfid/writer.py
import serial
import time
from app.config import SERIAL_PORT, BAUDRATE, TIMEOUT
from app.rfid.commands import READ_SINGLE_CMD
from app.utils.hex_conv import txt2hex


def calc_checksum(cmd: list) -> int:
    return sum(cmd[1:]) & 0xFF


def format_data(text: str) -> str:
    text = text.strip()
    # Max 24 bytes (12 words), safe limit for many tags
    if len(text) > 24:
        print("⚠️ Too long. Trimming to 24 chars.")
        text = text[:24]
    # Ensure even number of bytes (pad with underscore)
    if len(text) % 2 != 0:
        text += "_"
    return text


def write_tag(data: str):
    formatted = format_data(data)
    hex_payload = txt2hex(formatted)
    data_bytes = list(bytes.fromhex(hex_payload))

    word_count = len(data_bytes) // 2  # Each word is 2 bytes

    # Write command structure:
    # [AA] [00] [0x49] [00] [LEN] [BANK=03] [ADDR=00] [WORDCNT] + [DATA...] + [CHECKSUM] [DD]
    param = [0x03, 0x00, word_count] + data_bytes
    param_len = len(param)
    cmd = [0xAA, 0x00, 0x49, 0x00, param_len] + param
    checksum = calc_checksum(cmd)
    cmd.append(checksum)
    cmd.append(0xDD)

    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT) as ser:
        # Pre-select tag
        ser.write(READ_SINGLE_CMD)
        time.sleep(0.1)
        ser.flushInput()

        # Write to tag
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
            print(f"✅ Write successful: '{formatted}'")
            return True
        else:
            print(f"❌ Write failed, status code: {hex(status_code)}")
            return False
