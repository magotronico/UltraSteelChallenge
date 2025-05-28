# UltraSteelChallenge/app/rfid/rfid_module.py

from app.rfid.reader import *
from app.rfid.writer import write_tag

class RFIDModule:
    def write(self, text: str): 
        write_tag(text)
    
    def start_reading(self):
        """
        Start reading RFID tags continuously
        """
        def on_tag_detected(epc_ascii):
            print(f"✅ Tag leído: {epc_ascii}")
            # Add a function to save the tag to a database

        start_reading(callback=on_tag_detected)

    def stop_reading(self):
        """
        Stop reading RFID tags
        """
        stop_reading()

if __name__ == "__main__":
    rfid = RFIDModule()
    reading = False

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
            if not reading:
                rfid.start_reading()
                reading = True
                print("📡 Leyendo etiquetas... (presiona opción 3 para detener)")
            else:
                print("⚠ La lectura ya está en curso.")

        elif choice == '3':
            if reading:
                rfid.stop_reading()
                reading = False
                print("🛑 Lectura detenida.")
            else:
                print("⚠ La lectura no está activa.")

        elif choice == '4':
            if reading:
                rfid.stop_reading()
            print("👋 Saliendo...")
            break

        else:
            print("❌ Opción no válida.")

        time.sleep(1)
