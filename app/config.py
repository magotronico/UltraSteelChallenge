import os
from dotenv import load_dotenv
from datetime import datetime

# Load variables from .env
load_dotenv()

# Database configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

# Serial port settings
SERIAL_PORT = '/dev/ttyUSB0'
BAUDRATE = 115200

# Backend settings
BACKEND_URL = "http://localhost:8000/inventory/add"

# Inventory item settings
PRODUCT_NAME = "Suspension"
LOT_NUMBER = "0001"
RECEIVED_BY = "DC"
SKU_PREFIX = "P"
DATE = datetime.now().strftime('%Y%m%d')  # e.g., 20250523

# RFID command settings
READ_SINGLE_CMD = bytes([0xAA, 0x00, 0x22, 0x00, 0x00, 0x22, 0xDD])  # Inventory
READ_TAG_CMD = bytes([0xAA, 0x00, 0x39, 0x00, 0x03, 0x00, 0x0C, 0xDD])  # Read User bank, 24 bytes
WRITE_TAG_CMD_BASE = [0xAA, 0x00, 0x49, 0x00, 0x03, 0x00, 0x0C]  # Write User bank, 24 bytes
