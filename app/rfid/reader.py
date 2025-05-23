import serial
import time
import csv
import re
import requests
from datetime import datetime
from collections import defaultdict
from app.utils.sku_generator import generate_sku  # Update path as needed

# === CONFIG ===
PORT = '/dev/ttyUSB0'   # Update for Raspberry Pi or 'COM10' for Windows
BAUDRATE = 115200
CSV_FILE = 'epcs_contador_completo.csv'
BACKEND_URL = "http://localhost:8000/inventory/add"
PRODUCT_NAME = "Magic Wand XL"
LOT_NUMBER = "LOT2025A"
RECEIVED_BY = "JD"

# === GLOBALS ===
read_single_cmd = bytes([0xAA, 0x00, 0x22, 0x00, 0x00, 0x22, 0xDD])
epc_contador = defaultdict(int)
ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(1)  # Allow port to settle

# === UTILITIES ===
def extraer_epcs_limpios(data_bytes):
    """Extrae EPCs válidos de 96 bits que comienzan con E2."""
    epcs = []
    data_hex = ' '.join(f'{b:02X}' for b in data_bytes)
    matches = re.findall(r'(E2(?: [0-9A-F]{2}){11})', data_hex)
    for m in matches:
        epcs.append(m)
    return epcs

def send_to_backend(tag):
    payload = {
        "sku": generate_sku(PRODUCT_NAME),
        "lot": LOT_NUMBER,
        "received_by": RECEIVED_BY,
        "rfid_tag": tag,
        "received_at": datetime.utcnow().isoformat()
    }
    try:
        response = requests.post(BACKEND_URL, json=payload)
        print(f"📡 Enviado a backend: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Error enviando al backend: {e}")

# === MAIN FUNCTIONS ===
def listen_for_tags(save_to_csv=True, send_backend=True):
    print("🟢 Escaneando continuamente...")
    if save_to_csv:
        with open(CSV_FILE, 'w', newline='') as file:
            csv.writer(file).writerow(['EPC', 'Timestamp', 'Conteo total'])

    try:
        while True:
            ser.write(read_single_cmd)
            data = ser.read(128)
            if data:
                epcs = extraer_epcs_limpios(data)
                for epc in epcs:
                    epc_contador[epc] += 1
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    count = epc_contador[epc]
                    print(f"🔁 {epc} | Lectura total: {count} @ {timestamp}")

                    if save_to_csv:
                        with open(CSV_FILE, 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([epc, timestamp, count])

                    if send_backend:
                        send_to_backend(epc)
            else:
                print("… sin respuesta")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ Escaneo detenido por el usuario.")
        ser.close()

def test_serial_read(count=5):
    print(f"🧪 Test: leyendo {count} EPCs...")
    read_count = 0
    try:
        while read_count < count:
            ser.write(read_single_cmd)
            data = ser.read(128)
            if data:
                epcs = extraer_epcs_limpios(data)
                for epc in epcs:
                    read_count += 1
                    print(f"[{read_count}] {epc}")
                    if read_count >= count:
                        break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ Test interrumpido.")
    finally:
        print("✅ Test completo.")
        ser.close()

# === ENTRY POINT ===
if __name__ == "__main__":
    test_serial_read()
