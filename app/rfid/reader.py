# UltraSteelChallenge/app/rfid/reader.py

import serial
import time
from app.config import SERIAL_PORT, BAUDRATE, TIMEOUT
from app.rfid.commands import READ_SINGLE_CMD
from app.utils.hex_conv import hex2txt


def build_read_user_cmd(word_count=8):
    bank = 0x03
    start_addr = 0x00
    cmd_header = [0xAA, 0x00, 0x39, 0x00, 0x03, bank, start_addr, word_count]
    checksum = sum(cmd_header[1:]) & 0xFF
    return bytes(cmd_header + [checksum, 0xDD])


def read_tag(word_count=8, interval=1):
    read_cmd = build_read_user_cmd(word_count=word_count)

    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT) as ser:
        print("🔁 Starting continuous RFID read loop...\nPress Ctrl+C to stop.\n")
        try:
            while True:
                # Step 1: Select tag
                ser.write(READ_SINGLE_CMD)
                time.sleep(0.1)
                epc_response = ser.read(128)

                if len(epc_response) < 10:
                    print("… No tag detected")
                    time.sleep(interval)
                    continue

                ser.flushInput()

                # Step 2: Read user memory
                ser.write(read_cmd)
                time.sleep(0.2)
                response = ser.read(64)

                if len(response) < 10 or response[0] != 0xAA or response[-1] != 0xDD:
                    print("⚠️ Invalid or no response")
                    time.sleep(interval)
                    continue

                status = response[5]
                if status != 0x10:
                    print(f"❌ Read failed: status {hex(status)}")
                    time.sleep(interval)
                    continue

                data_payload = response[6:-2]
                if not data_payload:
                    print("⚠️ No data payload")
                    time.sleep(interval)
                    continue

                hex_string = ''.join(f'{b:02X}' for b in data_payload)
                decoded = hex2txt(hex_string)
                print(f"📦 Tag Read: {decoded}")
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n🛑 Reading stopped by user.")

if __name__ == "__main__":
    while True:
        data = read_tag()
        if data:
            print("📦 Data:", data)
        time.sleep(1)
