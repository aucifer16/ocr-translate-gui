# OCR & Translate Overlay GUI

This is a desktop application that performs real-time OCR (Optical Character Recognition) for **Thai**, **English**, and **Japanese** text. It translates the recognized text to Thai and displays the translated result as an overlay on the original screen location.

## 📌 Features

- 🧠 OCR with support for `eng`, `tha`, `jpn` using Tesseract OCR
- 🌐 Translation using Google Translate (via `googletrans`)
- 💬 Overlay the translated text at the same screen region
- 🖱️ Select custom screen zone for OCR
- 🔁 Automatically refreshes every 2 seconds
- ⏸️ Pause / Resume OCR
- 💾 Save OCR results to `.txt`
- 🧹 Clear output

## 📂 Folder Structure
ocr-project/ ├── runocr.py ├── tesseract/ │ ├── tesseract.exe │ └── tessdata/ │ ├── eng.traineddata │ ├── tha.traineddata │ └── jpn.traineddata ├── requirements.txt ├── README.md


> ℹ️ **Tesseract OCR is bundled in the `tesseract/` folder for portability.**

## 🛠 Requirements

- Python 3.7+
- Windows 64-bit
- Installed packages in `requirements.txt`

## 🔧 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ocr-translate-gui.git
   cd ocr-translate-gui


   pip install -r requirements.txt


   python runocr.py


### 🧠 How it Works
Select a screen zone using mouse

The app will capture that region every 2 seconds

Performs OCR, translates the text to Thai

Displays translated result as temporary overlay (1 second)

### 🧑‍💻 Developer
Sittiphong Pornudomthap
Email: sittiphong@pnru.ac.th


### 📦 Packaging to .exe (Optional)
pyinstaller --noconfirm --onefile --windowed --add-data "tesseract;tesseract" runocr.py
