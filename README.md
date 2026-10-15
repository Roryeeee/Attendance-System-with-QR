# 🛠️ Attendance System

This Project was really a good experience for me to test my skills that i had learned and bonus to that got to use it as a hackathon's official Attendence system at (Bernhack 2025)
A lightweight, GUI-powered Python application to manage QR-based attendance tracking during hackathons or similar events. It includes tools to:

- ✅ Generate unique QR codes for participants, organizers, and volunteers.
- ✅ Register and manage users in a local SQLite database.
- ✅ Scan QR codes to track check-ins using a webcam.
- ✅ Export attendance data to a CSV file for reporting.

---

## 📁 Project Structure

```
├── main_gui.py # Central GUI to launch various operations
├── QR_Generator.py # Generate QR codes with user info
├── register_users.py # Register, delete, and manage users
├── QR_code_scanning.py # Scan QR codes to mark attendance
├── export_attendence.py # Export check-in records to CSV
├── attendance.db # SQLite database storing all user info
├── attendance_log.csv # (Generated) Exported attendance file
└── qrs/ # (Generated) Folder where QR PNGs are saved
```

---

## 🧰 Requirements

Install the dependencies using:

```bash
pip install -r requirements.txt
```
---
##Required Python Libraries:

tkinter (usually preinstalled)

qrcode

uuid

sqlalchemy

opencv-python

pyzbar

pandas66

###Note: pyzbar requires native ZBar libraries. Install them as follows:

macOS: brew install zbar

Ubuntu: sudo apt install libzbar0

Windows: Install ZBar DLLs manually and ensure they're in your PATH


##🚀 How to Run
Launch the main control panel:

```
py
python main_gui.py
```
From there, you can:

📷 Generate QR Code: For new participants or organizers

📝 Register / Manage Users: Add or delete users from the database

📡 Run Attendance Scanner: Use your webcam to scan and mark check-ins

📤 Export Attendance: Generate a CSV report of all attendance data


##📷 QR Generation
QR_Generator.py creates a PNG QR code containing:

```json
{
  "user_id": "a1b2c3d4",
  "name": "Jane Doe",
  "role": "Participant",
  "team": "TeamRocket"
}
```
All QR codes are saved to your ~/Documents/qrs folder by default.


##🔍 Attendance Scanner
QR_code_scanning.py uses your webcam to scan QR codes and:

✅ Marks user as checked in

⚠️ Prevents duplicate check-ins

❌ Warns if QR belongs to an unknown user

##🧠 Local Database
All user data is stored locally using SQLite in attendance.db.

Supported roles include:

participant

organizer

mentor

evaluator

##📤 Exporting Data
Run export_attendence.py to generate:

```csv
attendance_log.csv
```
Fields include:
User ID
Name
Role
Team
Check-in Status
Check-in Time
