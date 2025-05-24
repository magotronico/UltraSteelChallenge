# UltraSteelChallenge/app/rfid/rfid_module.py

from app.rfid.reader import read_tag
from app.rfid.writer import write_tag
from app.utils.hex_conv import txt2hex, hex2txt

class RFIDModule:
    def read(self) -> str | None:
        hex_data = read_tag()
        if hex_data:
            return hex2txt(hex_data)
        return None

    def write(self, text: str):
        hex_data = txt2hex(text)
        write_tag(hex_data)

if __name__ == "__main__":
    rfid = RFIDModule()

    # Test write
    sample_data = "ABC123-LOT45-20240522-JD"

    # Write sample data to tag
    print(f"📝 Writing tag: {sample_data}")
    rfid.write(sample_data)

    # Read back the tag
    print("🔍 Reading tag...")
    result = rfid.read()

    # Display the result
    if result:
        print(f"✅ Read: {result}")
    else:
        print("❌ No tag read")
