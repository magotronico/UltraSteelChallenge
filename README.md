# UltraSteelChallenge

## 📦 RFID Traceability API & Demo Website

This project demonstrates how RFID technology can be used to support ISO 9001 compliance through automated traceability. It includes a backend API built with FastAPI and a demo website using templates from [v0.dev](https://v0.dev). The system is designed to run on a Raspberry Pi 4 connected to an R200 UHF RFID reader.

---

## 📌 Purpose

The goal of this project is to show how RFID enhances traceability in manufacturing, warehousing, or logistics workflows, helping organizations meet the traceability and documentation requirements of **ISO 9001**.

---

## ⚙️ Tech Stack

### Backend
- **Language:** Python 3.11
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** (Add your choice here — SQLite, PostgreSQL, etc.)
- **RFID Integration:** Raspberry Pi 4 + R200 UHF RFID reader

### Frontend
- **UI Templates:** [v0.dev](https://v0.dev)
- **Framework:** (e.g., plain HTML/CSS/JS, React, or other if applicable)

---

## 🔍 Features

- ✅ REST API for RFID tag data management
- ✅ Real-time tracking from RFID reader
- ✅ Web interface to visualize tag reads and device activity
- ✅ Logs to support ISO 9001 audit and compliance processes
- ✅ Modular codebase for easy extension

---

## 📈 ISO 9001 Compliance

This project demonstrates how RFID traceability aligns with ISO 9001 by supporting:

- **Clause 8.5.2:** Product identification and traceability
- **Clause 7.5:** Documented information management
- **Clause 9:** Evidence-based decision making
- **Clause 10.2:** Corrective actions through complete traceability logs

---

## 🚀 Getting Started

### Prerequisites

- Raspberry Pi 4
- R200 UHF RFID reader
- Python 3.11
- pipenv or virtualenv (optional but recommended)

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/magotronico/UltraSteelChallenge.git
   cd UltraSteelChallenge
   ```

2. **Set up Python environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the API**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Run the web frontend**
   - Navigate to the frontend folder and follow instructions to serve the demo site (if React or similar is used).

---

## 🧪 Development

- Backend code is located in `app/`
- Frontend code is in `frontend/`
- RFID read scripts are in `rfid/`

---

## 🛡️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📬 Contact

For questions or collaboration, open an issue or reach out via A00831905@exatec.tec.mx

