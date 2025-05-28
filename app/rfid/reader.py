# UltraSteelChallenge/app/rfid/reader.py

# Libraries
import time
import serial
import re
import threading
from app.config import SERIAL_PORT, BAUDRATE

# Module variables
_reading = False
_reader_thread = None
_ser = None


# FUNCTIONS
# Split the data string into individual RFID tags
def split_tags(data_string: str) -> list:
    """
    Divide la cadena de datos en etiquetas RFID individuales.
    """
    data_string = data_string.strip()
    return re.findall(r'AA(?: [0-9A-F]{2})*? DD', data_string)

# Read loop function that continuously reads RFID tags
def _read_loop(callback, port, baudrate, interval):
    global _reading, _ser
    read_cmd = bytes([0xAA, 0x00, 0x22, 0x00, 0x00, 0x22, 0xDD])

    try:
        _ser = serial.Serial(port, baudrate, timeout=1)
        print("📡 Starting continuous reading of RFID tags...")

        while _reading:
            _ser.write(read_cmd)
            time.sleep(1)
            response = _ser.read(64)

            if response:
                response_str = ' '.join(f'{b:02X}' for b in response)
                tags = split_tags(response_str)
                for tag in tags:
                    tag_parts = tag.split(" ")
                    try:
                        header_index = tag_parts.index('AA')
                        epc_len = int(tag_parts[header_index + 2], 16) // 2
                        epc_data = tag_parts[header_index + 8:header_index + 3 + epc_len]
                        epc_ascii = ''.join(chr(int(b, 16)) for b in epc_data if 32 <= int(b, 16) <= 126)
                        if callback:
                            callback(epc_ascii)
                    except Exception as e:
                        print("⚠ EPC could not been extracted:", e)
            else:
                print("❌ No answer detected from reader.")

            time.sleep(interval)

    except Exception as err:
        print("⚠ Error reading the RFID:", err)
    finally:
        if _ser and _ser.is_open:
            _ser.close()
        print("🛑 Reading tags stopped.")

# Start reading RFID tags in a separate thread
def start_reading(callback=None, port=SERIAL_PORT, baudrate=BAUDRATE, interval=1):
    """
    Start reading RFID tags continuously in a separate thread.
    Parameters:
        callback (function): Function to call when a tag is detected.
        port (str): Serial port to use for reading.
        baudrate (int): Baud rate for the serial connection.
        interval (int): Time interval between reads in seconds.
    Returns:
        None
    """
    global _reading, _reader_thread

    if _reading:
        print("⚠ La lectura ya está en curso.")
        return

    _reading = True
    _reader_thread = threading.Thread(target=_read_loop, args=(callback, port, baudrate, interval), daemon=True)
    _reader_thread.start()

# Stop reading RFID tags and close the serial connection
def stop_reading():
    """
    Detiene la lectura continua de RFID.
    """
    global _reading, _ser
    _reading = False
    if _reader_thread:
        _reader_thread.join()
    if _ser and _ser.is_open:
        _ser.close()
    print("🔴 Lectura RFID detenida manualmente.")
