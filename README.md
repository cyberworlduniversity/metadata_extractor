# 🧾 Metadata Extractor

> **Tool #11 in the Kit** — Extract hidden metadata from image files including camera info, date/time, and GPS location data.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![GitHub](https://img.shields.io/badge/GitHub-hemanathan115-black.svg)](https://github.com/hemanathan115)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 What It Does

The **Metadata Extractor** reads hidden EXIF and metadata embedded inside image files and presents it in a clean, structured format. Think of it as X-ray vision for your photos!

### Extracted Data Includes:
| Category | Details |
|---|---|
| 📷 **Camera Info** | Make, Model, Lens, Focal Length, ISO, Aperture |
| 📅 **Date & Time** | Original capture date, digitized date |
| 📍 **GPS Location** | Latitude, Longitude, Google Maps link |
| 🖼️ **Image Properties** | Resolution, Format, Color Mode |
| 📁 **File Info** | Size, Path, Last Modified |

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/hemanathan115/metadata-extractor.git
cd metadata-extractor

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Usage

### Basic Usage
```bash
python metadata_extractor.py photo.jpg
```

### JSON Output
```bash
python metadata_extractor.py photo.jpg --format json
```

### Save Report
```bash
python metadata_extractor.py photo.jpg --save report.json
```

### Batch Process Multiple Images
```bash
python metadata_extractor.py img1.jpg img2.jpg img3.png --batch
```

### Process All JPGs in a Folder
```bash
python metadata_extractor.py *.jpg --batch --save batch_report.json
```

---

## 📦 Dependencies

```
Pillow>=9.0.0
exifread>=3.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 📸 Sample Output

```
============================================================
🧾  METADATA EXTRACTOR - RESULTS
============================================================

📁 File Information
----------------------------------------
  filename                  : photo.jpg
  file_size                 : 3.45 MB
  last_modified             : 2024-01-15 10:30:22

📷 Camera Information
----------------------------------------
  Make                      : Apple
  Model                     : iPhone 14 Pro
  FocalLength               : 6.86
  ISOSpeedRatings           : 50

📅 Date & Time
----------------------------------------
  DateTimeOriginal          : 2024:01:15 10:30:22

📍 GPS / Location
----------------------------------------
  DecimalLatitude           : 13.0827
  DecimalLongitude          : 80.2707
  GoogleMapsLink            : https://www.google.com/maps?q=13.0827,80.2707

============================================================
✅ Extraction Complete!
============================================================
```

---

## 🛡️ Supported Formats

- `.jpg` / `.jpeg`
- `.png`
- `.tiff` / `.tif`
- `.heic` (with Pillow-heif plugin)
- `.webp`

---

## 📁 Project Structure

```
metadata-extractor/
├── metadata_extractor.py   # Main script
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
└── LICENSE                 # MIT License
```

---

## 🔒 Privacy Notice

This tool runs **entirely offline** on your local machine. No data is uploaded or transmitted anywhere.

---

## 👨‍💻 Author

**Hemanathan**  
GitHub: [@hemanathan115](https://github.com/hemanathan115)

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
