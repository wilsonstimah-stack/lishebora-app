# Build LisheBora Android APK - Multiple Options

## Option 1: Google Colab (Easiest - No Setup)

1. Go to https://colab.research.google.com
2. Create new notebook
3. Run these cells:

```python
# Cell 1: Setup
!pip install buildozer cython==0.29.33
!sudo apt-get update
!sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config
```

```python
# Cell 2: Upload your files
from google.colab import files
uploaded = files.upload()  # Upload main.py, lishebora_icon.png, buildozer.spec
```

```python
# Cell 3: Build
!buildozer android release
```

```python
# Cell 4: Download APK
files.download('bin/lishebora-1.0.0-arm64-v8a-release.aab')
```

---

## Option 2: Setup WSL Properly

Open PowerShell as Admin:
```powershell
wsl --install -d Ubuntu
```

Then in Ubuntu terminal:
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git zip unzip openjdk-17-jdk
sudo apt install -y autoconf automake libtool pkg-config libffi-dev libssl-dev

pip3 install buildozer cython==0.29.33

cd /mnt/c/Users/ADMIN/Desktop/INFORMATICS
buildozer android release
```

---

## Option 3: Use Replit (Online IDE)

1. Go to https://replit.com
2. Create Python project
3. Upload files
4. Use Shell to run buildozer

---

## Output File
After build completes, your standalone APK is at:
`bin/lishebora-1.0.0-arm64-v8a-release.aab`

This is ready to upload to Google Play Store!
