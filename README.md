# ScannerDark 🔍🌐

**ScannerDark** is a Python-based network and port scanner with a graphical interface built using **Tkinter**.  
It allows users to scan local networks, detect active hosts, check common open ports, and generate PDF reports.

This project was developed for educational purposes, focusing on **computer networks**, **Python programming**, and **GUI development**.

---

## ✨ Features

- 🖧 Network scan to detect active devices
- 🔓 Port scanning (SSH, HTTP, HTTPS, RDP)
- 🪟 Graphical interface using Tkinter
- 📄 PDF report generation
- ⚡ Multi-threaded scanning for better performance
- 🌙 Dark-themed interface

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** (GUI)
- **Socket**
- **Threading**
- **ReportLab** (PDF generation)
- **Subprocess**
- **Linux / macOS compatible**

---

## 📂 Project Structure


---

## 💻 Installation & Usage

### 🐧 Linux

#### Requirements
- Python 3.9 or newer
- pip

#### Steps
```bash
git clone https://github.com/camilatrindad/scanner-dark.git
cd scanner-dark
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scanner_dark.py

---

This application is distributed as source code for macOS.

Requirements
```

### macOS

Python 3.9 or newer (from https://www.python.org
)

Steps
git clone https://github.com/camilatrindad/scanner-dark.git
cd scanner-dark
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scanner_dark.py


If macOS blocks network access, allow Python in
System Settings → Privacy & Security.


📄 PDF Report

The application can generate a PDF report containing:

Date and time of the scan

List of active devices

Open ports detected

The PDF file is saved in the same directory where the program is executed.


⚠️ Notes & Limitations

Some network scans may require administrator privileges.

Port scanning is limited to common ports by default.

Network behavior may vary depending on firewall rules and OS permissions.

The project is intended for educational and ethical use only.


🎓 Academic Context

This project was developed as part of the Computer Networks course at
IFRN – Federal Institute of Rio Grande do Norte.

It demonstrates practical knowledge of:

Network concepts

Socket programming

Multithreading

Cross-platform Python applications


📌 Future Improvements

Custom port range scanning

Export results to CSV

Improved macOS compatibility

Executable and installer versions

Network interface selection


👩‍💻 Author

Camila Trindade
Computer Networks Student – IFRN

GitHub: @camilatrindad

📜 License

This project is for educational purposes.
You are free to study, modify, and improve the code.
