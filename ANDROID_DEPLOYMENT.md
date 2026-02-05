# LisheBora & LishePro - Android Deployment Guide

## Overview

This guide explains how to build and deploy the LisheBora (User App) and LishePro (Professional Portal) as standalone Android mobile applications.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LisheBora Kenya                          │
├─────────────────────────┬───────────────────────────────────┤
│     LisheBora App       │        LishePro App               │
│   (End User/Client)     │   (Nutritionist/Professional)     │
├─────────────────────────┼───────────────────────────────────┤
│ • Health Assessment     │ • Dashboard & Analytics           │
│ • BMI & MUAC Calc       │ • User Management                 │
│ • Personalized Diet     │ • Answer User Questions           │
│ • Food Diary            │ • Generate Reports                │
│ • Nutrition Support     │ • Settings                        │
└─────────────────────────┴───────────────────────────────────┘
```

---

## Files Structure

```
INFORMATICS/
├── client_app.py          # Desktop Tkinter version (User)
├── developer_app.py       # Desktop Tkinter version (Professional)
├── lishebora_mobile.py    # Android Kivy version (User)
├── lishepro_mobile.py     # Android Kivy version (Professional)
├── common_utils.py        # Shared utilities & constants
├── backend_manager.py     # Local storage & sync
├── buildozer.spec         # Android build configuration
└── ANDROID_DEPLOYMENT.md  # This file
```

---

## Prerequisites

### For Windows Users
1. **WSL2 (Windows Subsystem for Linux)**
   ```powershell
   wsl --install -d Ubuntu
   ```

2. **In Ubuntu/WSL2, install dependencies:**
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv git zip unzip openjdk-17-jdk
   sudo apt install -y autoconf automake libtool pkg-config
   sudo apt install -y libffi-dev libssl-dev
   ```

3. **Install Buildozer:**
   ```bash
   pip install --upgrade buildozer
   pip install --upgrade cython==0.29.33
   ```

4. **Install Android SDK (automatic with buildozer)**

---

## Building LisheBora (User App)

### Step 1: Prepare the Project
```bash
# Navigate to project directory
cd /mnt/c/Users/ADMIN/Desktop/INFORMATICS

# Create main.py for Kivy app
cp lishebora_mobile.py main.py
```

### Step 2: Initialize Buildozer
```bash
buildozer init
```

### Step 3: Build the APK
```bash
# Debug build (for testing)
buildozer android debug

# Release build (for distribution)
buildozer android release
```

### Step 4: Find Your APK
The APK will be in:
```
./bin/lishebora-1.0.0-arm64-v8a-debug.apk
```

---

## Building LishePro (Professional App)

Repeat the above steps but:
1. Replace `main.py` with `lishepro_mobile.py`
2. Update `buildozer.spec`:
   - `title = LishePro`
   - `package.name = lishepro`

---

## Installing on Android Device

### Option 1: Direct Install
1. Copy APK to your phone
2. Enable "Install from Unknown Sources" in Settings
3. Tap the APK file to install

### Option 2: ADB Install
```bash
adb install bin/lishebora-1.0.0-arm64-v8a-debug.apk
```

---

## Desktop Testing (Windows/Mac/Linux)

### Run LisheBora Desktop (Tkinter)
```bash
python client_app.py
```

### Run LishePro Desktop (Tkinter)
```bash
python developer_app.py
```

### Run LisheBora Mobile Preview (Kivy)
```bash
pip install kivy
python lishebora_mobile.py
```

### Run LishePro Mobile Preview (Kivy)
```bash
python lishepro_mobile.py
```

---

## App Features

### LisheBora (User App)
| Feature | Description |
|---------|-------------|
| 🏠 Home | Health assessment with BMI & MUAC calculations |
| 🥗 My Diet | Personalized Kenyan meal plans |
| 📝 Food Diary | Track daily food intake |
| 💬 Support | Chat with nutritionists |
| 👤 Profile | User settings and status |

### LishePro (Professional App)
| Feature | Description |
|---------|-------------|
| 📊 Dashboard | Overview of user statistics |
| 👥 Users | Manage and view user profiles |
| ❓ Questions | Answer user nutrition questions |
| 📈 Reports | Generate nutrition reports |
| ⚙️ Settings | Account configuration |

---

## Consent & Data Protection

Both apps include:
- ✅ Informed consent screen with checkbox toggle
- ✅ Professional consent text aligned with Kenya Data Protection Act, 2019
- ✅ Clear explanation of data usage
- ✅ User rights disclosure

---

## MOH Kenya Alignment

The apps follow Kenya Ministry of Health guidelines:
- Age brackets per Kenya MIYCN guidelines
- MUAC cutoffs per WHO/MOH standards
- Kenyan food database (Sukuma, Ugali, Omena, etc.)
- Nutritional status classifications

---

## Troubleshooting

### Kivy Window Issues
```bash
# If window doesn't render properly
pip install kivy[full]
```

### Build Fails
```bash
# Clean and rebuild
buildozer android clean
buildozer android debug
```

### Missing SDK
```bash
# Let buildozer download automatically
buildozer android debug  # First run downloads SDK
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 2024 | Initial release with BMI, MUAC, Diet Plans |

---

## Contact

For support or feature requests, contact the LisheBora development team.

**LisheBora Kenya** - *Good Nutrition for All*
