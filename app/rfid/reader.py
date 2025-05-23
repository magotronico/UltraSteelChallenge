import serial
import requests
from datetime import datetime
from app.utils.sku_generator import generate_sku

ser = serial.Serial('/dev/ttyS0', 9600)

def listen_for_tags():
    while True:
        if ser.in_waiting > 0:
            tag = ser.readline().decode().strip()
            print(f"Detected tag: {tag}")
            send_to_backend(tag)

def send_to_backend(tag):
    payload = {
        "sku": generate_sku("Magic Wand XL"),
        "lot": "LOT2025A",
        "received_by": "JD",
        "rfid_tag": tag,
        "received_at": datetime.utcnow().isoformat()
    }
    response = requests.post("http://localhost:8000/inventory/add", json=payload)
    print(response.json())

def test_serial_read(count=5):
    print(f"Starting test: reading {count} tags...")
    read_count = 0
    while read_count < count:
        if ser.in_waiting > 0:
            tag = ser.readline().decode().strip()
            print(f"[{read_count + 1}] Detected tag: {tag}")
            read_count += 1
    print("Test complete.")

if __name__ == "__main__":
    test_serial_read()