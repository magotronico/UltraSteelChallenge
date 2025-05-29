# UltraSteelChallenge/app/rfid/rfid_module.py

from app.rfid.reader import *
from app.rfid.writer import write_tag
from app.database.client import init_db, add_item
from app.models.item import InventoryItem as item

class RFIDModule:
    def __init__(self):
        """
        Initialize the RFID module
        """
        self.reading = False

    def write(self, text: str): 
        """
        Write text to an RFID tag
        :param text: Text to write to the tag
        """
        write_tag(text)
    
    def start_reading(self):
        """
        Start reading RFID tags continuously
        """
        if self.reading:
            print("⚠ Reading is already active.")
            return
        
        def on_tag_detected(epc_ascii):
            print(f"✅ Tag leído: {epc_ascii}")
            new_tag = item.from_epc_ascii(epc_ascii)
            result = add_item(new_tag)
            if result == 1:
                print("✅ Tag added to the database.")
            else:
                print("❌ Tag already exists in the database.")

        start_reading(callback=on_tag_detected)
        self.reading = True

    def stop_reading(self):
        """
        Stop reading RFID tags
        """
        if self.reading:
            stop_reading()
            self.reading = False
        else:
            print("⚠ Reading is not active.")
        

if __name__ == "__main__":
    rfid = RFIDModule()

    while True:
        print("\n📋 MENU RFID")
        print("1. Escribir etiqueta")
        print("2. Iniciar lectura continua")
        print("3. Detener lectura")
        print("4. Salir")

        choice = input("Selecciona una opción: ")

        if choice == '1':
            data = input("🔤 Ingresa el texto a escribir en la etiqueta: ")
            rfid.write(data)
            print("✅ Etiqueta escrita.")

        elif choice == '2':
            if not rfid.reading:
                rfid.start_reading()
            else:
                print("⚠ Reading is already active.")

        elif choice == '3':
            if rfid.reading:
                rfid.stop_reading()
            else:
                print("⚠ Reading is not active.")

        elif choice == '4':
            if rfid.reading:
                rfid.stop_reading()
            print("👋 Saliendo...")
            break

        else:
            print("❌ Opción no válida.")

        time.sleep(1)
