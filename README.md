# UltraSteelChallenge

[![Tech Stack](https://skillicons.dev/icons?i=nextjs,typescript,tailwind,fastapi,python,raspberrypi&theme=light)](https://skillicons.dev)

## 📦 RFID Traceability API & Demo Website

This project demonstrates how RFID technology can be used to support ISO 9001 compliance through automated traceability. It includes a backend API built with FastAPI and a frontend dashboard built with Next.js and React. The system is designed to run on a Raspberry Pi 4 connected to an R200 UHF RFID reader.

---

## 📌 Purpose

The goal of this project is to show how RFID enhances traceability in manufacturing, warehousing, or logistics workflows, helping organizations meet the traceability and documentation requirements of **ISO 9001**.

---

## ⚙️ Tech Stack

### Backend
- **Language:** Python 3.11
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** CSV (temporary solution for MVP)
- **RFID Integration:** Raspberry Pi 4 + R200 UHF RFID reader

### Frontend
- **Framework:** Next.js with React
- **Language:** TypeScript (ES6 target)
- **Styling:** Tailwind CSS
- **UI Templates:** [v0.dev](https://v0.dev)
- **Deployment:** Local development (Vercel planned for production)

---

## 🔍 Features

- ✅ REST API for RFID tag data management
- ✅ Real-time tracking from RFID reader
- ✅ Interactive dashboard with KPIs and inventory management
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
- Node.js 18+ and npm/yarn
- pipenv or virtualenv (optional but recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/magotronico/UltraSteelChallenge.git
   cd UltraSteelChallenge
   ```

### Backend Setup

2. **Set up Python environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the FastAPI backend**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup

4. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

5. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

6. **Configure environment variables**
   ```bash
   # Create .env.local file
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

7. **Run the Next.js frontend**
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   
   The frontend will be available at `http://localhost:3000`

---

## 🧪 Development

- Backend code is located in `app/`
- Frontend code is in `frontend/`
- RFID read scripts are in `app/rfid/`
- Database client scripts in `app/api/database/`

---

## 📸 Screenshots

*Screenshots and images will be added here to showcase the dashboard interface, RFID tracking features, and system architecture.*

<div align="center">
  <img src="Resources\SignIn.png" alt="Sign-In Overview" width="350" style="margin: 0 10px;">
  <img src="Resources\UltraSteelWebApp.jpg" alt="Dashboard Overview" width="350" style="margin: 0 10px;">
  <img src="Resources\UltraSteelWebApp3.jpg" alt="RFID Tracking" width="350" style="margin: 0 10px;">
  <img src="Resources\UltraSteelWebApp2.jpg" alt="Inventory Management" width="350" style="margin: 0 10px;">
</div>

<div align="center">
  <em>Sign-In Overview | Dashboard Overview | RFID Tracking | Inventory Management</em>
</div>

---

## 🚧 Future Plans

### Database & Infrastructure
- **Database Migration:** Replace CSV with Supabase database
- **ORM Integration:** Modify `app/api/database/client.py` to handle all connections with proper ORM practices
- **Production Deployment:** Implement tunnelSSL for Raspberry Pi 4 backend with Vercel frontend deployment

### Authentication & Security
- **Sign-In Integration:** Implement valid authentication system
- **SSL/HTTPS:** Resolve deployment challenges with educational network limitations

### Dashboard Enhancements
- **Advanced KPIs:** Expand dashboard with more Key Performance Indicators
- **OKRs Integration:** Add Objectives and Key Results tracking
- **Real-time Analytics:** Enhanced data visualization and reporting

### User Experience
- **Advanced Search:** Replace search input with comprehensive filtering system for inventory items
- **Settings Panel:** 
  - Profile management
  - RFID tag module port administration
  - API_URL configuration for local deployments
- **Export Functionality:** AI-generated reports on production performance based on input/output mapping

### Error Handling
- **Robust Validation:** Better management of edge cases (non-existent materials, duplicate entries)
- **User Feedback:** Improved error messaging and user guidance

---

## 🚨 Known Limitations

- **Network Constraints:** Educational network limitations prevent direct SSL tunneling
- **Deployment:** Vercel blocks HTTP requests, and ngrok auto-auth doesn't resolve SSL validation issues
- **Database:** Currently using CSV as temporary database solution

---

## 🛡️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📬 Contact

For questions or collaboration, open an issue or reach out via A00831905@exatec.tec.mx