# UltraSteelChallenge/app/config.py
from datetime import datetime

# Serial port settings
SERIAL_PORT = 'COM6'
BAUDRATE = 115200
TIMEOUT = 1

# Inventory item settings
DATE = datetime.now().strftime('%j%y')  # e.g., 00325 for Jan 3, 2025
