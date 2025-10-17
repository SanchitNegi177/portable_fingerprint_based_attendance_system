# 🖐️ Portable Fingerprint-Based Attendance System

A **secure and portable fingerprint-based attendance system** built using **Python**, **Pygame GUI**, and a **biometric sensor**.  
It enables **real-time fingerprint authentication**, **encrypted data storage**, and **fraud-prevention mechanisms** to ensure accurate student attendance logging.

---

## 🚀 Features

- GUI-based interface using **Pygame**
- **Fingerprint enrollment**, validation, and deletion
- Encrypted storage of fingerprints using **AES-128 (CBC mode)** with **HMAC-SHA256**
- Prevents duplicate attendance marking
- **Admin authentication** for secure system access
- Optional integration with **MySQL** for data upload
- Real-time date and time display
- Confirmation dialogs and error-handling messages

---

## 🧠 System Overview

This project replaces manual attendance with a **biometric verification system** using a **fingerprint sensor (R307)** connected to a **Raspberry Pi**.

Each student:
- Enrolls their fingerprint once (a unique UID is assigned).
- When validating, the scanned fingerprint is compared with encrypted templates.
- On a successful match, attendance is recorded automatically.

---

## 🔐 Security Implementation

The system uses **AES-128 in CBC mode with HMAC-SHA256** through the `cryptography.fernet` module.

### 🔸 Encryption Workflow
1. Fingerprint template → binary data  
2. Binary data encrypted using `Fernet(key)` → ciphertext  
3. Base64 encoded ciphertext → stored in `fingerprints.json`  
4. On validation → decrypted and compared with live scan

This ensures:
- **Confidentiality:** via AES-128 encryption  
- **Integrity:** via HMAC-SHA256 authentication  
- **Tamper protection:** decryption fails if ciphertext is modified

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/SanchitNegi177/portable_fingerprint_based_attendance_system.git
cd portable_fingerprint_based_attendance_system
```
2️⃣ Install Dependencies
```bash
pip install pyfingerprint cryptography pygame mysql-connector-python
```
3️⃣ Connect Hardware

Attach the fingerprint sensor (R307 or compatible) via /dev/ttyUSB0
Ensure baud rate = 57600
Verify connection:
```python
from pyfingerprint.pyfingerprint import PyFingerprint
PyFingerprint('/dev/ttyUSB0', 57600).verifyPassword()
```
4️⃣ Run the Application
```python
python main_menu.py
```

## 🖥️ How It Works

### 🧩 Enrollment
- Scan finger twice to register a new student UID  
- Fingerprint template is encrypted and stored in `fingerprints.json`

### ✅ Validation
- Place finger on the sensor  
- If match found → attendance recorded in `verified_uids.json`  
- Duplicate scans are ignored  
- Unrecognized fingerprints trigger an error message

### ☁️ Upload
- Admin can upload attendance data to a connected **MySQL database**

---

## 📁 Project Structure

| File | Description |
|------|-------------|
| `fingerprint_validation.py` | Verifies fingerprints and marks attendance |
| `fingerprint_registration.py` | Enrolls, re-enrolls, or deletes fingerprints |
| `main_menu.py` | Launches the GUI main menu |
| `user_interface.py` | Handles GUI components (buttons, colors, fonts) |
| `admin.py` | Admin setup and authentication |
| `data_to_upload.py` | Uploads attendance data |
| `fingerprints.json` | Stores encrypted fingerprint templates |
| `verified_uids.json` | Stores marked attendance records |

---

## 🧩 Workflow

1. Launch the main menu  
2. Enroll student fingerprints  
3. Validate fingerprints for attendance  
4. Data is securely saved and can be uploaded to the database  
5. Exit using the **Quit** button (with confirmation dialog)

---

## 📜 License

This project is **open-source** and available for **educational and personal use**.

---

## 🙏 Acknowledgements

- [PyFingerprint Library](https://github.com/bastianraschke/pyfingerprint)  
- [Cryptography.io](https://cryptography.io/)  
- [Pygame](https://www.pygame.org/)  
- [Raspberry Pi Foundation](https://www.raspberrypi.org/)
