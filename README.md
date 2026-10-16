# 🎵 Music Robot AMR KUKA

[🇲🇽 Versión en Español](README.md)

Web application developed with **Python + Flask** to manage, process, and replace audio files used by **KUKA AMRs**.

The application allows users to download audio, preview it, optionally select and trim a section, convert it to the formats required by the robot, and transfer the resulting files directly to the AMR using **SSH/SFTP**.

---

## 📌 Project Overview

The objective of this project is to simplify the process of changing music and sound files on KUKA AMRs.

Instead of manually downloading, editing, converting, and transferring audio files, the application centralizes these operations in a single web interface.

### General workflow

```text
Download audio
      ↓
Generate source file
      ↓
Preview / listen
      ↓
Is trimming required?
   ↓           ↓
  Yes          No
   ↓           ↓
 Trim      Full audio
      \       /
       ↓     ↓
Process audio
       ↓
Generate files
AW100 / AW200
       ↓
Enter robot IP
       ↓
SSH/SFTP connection
       ↓
Upload files to AMR
```

---

## 🚀 Features

The application currently supports:

- Audio downloading.
- Source audio file generation.
- Audio preview and playback.
- Audio section selection.
- Optional audio trimming.
- Using the complete audio without trimming.
- Audio processing with FFmpeg.
- Generation of the required AW100 and AW200 files.
- Robot IP input through the web interface.
- SSH connection to the AMR.
- File transfer using SFTP.
- Local execution on Windows.
- Local execution on Linux.
- Deployment using Docker on a Linux server.

---

## 🛠️ Technologies

The project mainly uses:

- Python
- Flask
- Gunicorn
- FFmpeg
- FFprobe
- SSH / SFTP
- HTML
- CSS
- JavaScript
- Docker
- Docker Compose

---

## ✅ Requirements

Before running the application, the following components are required:

- Python 3
- pip
- Git
- FFmpeg
- FFprobe
- Network access to the KUKA AMRs
- Docker and Docker Compose for containerized deployment

Verify the installed tools with:

```bash
python --version
pip --version
ffmpeg -version
ffprobe -version
```

On Linux, it may be necessary to use:

```bash
python3 --version
pip3 --version
```

> **Important:** The computer or server running the application must have network connectivity to the AMRs in order to transfer files using SSH/SFTP.

---

## 📁 Project Structure

```text
Music_Robot_AMR_KUKA/
│
├── App.py
├── compose.yaml
├── Dockerfile
├── gunicorn.conf.py
├── README.md
├── README_EN.md
├── requirements.txt
│
├── models/
├── services/
├── static/
├── storage/
├── templates/
└── test/
```

### Main directories

**`models/`**

Contains the models used by the application.

**`services/`**

Contains the application logic, including audio processing and communication with the robots.

**`templates/`**

Contains the HTML pages used by Flask.

**`static/`**

Contains web interface resources such as CSS and JavaScript.

**`storage/`**

Contains audio files used and generated during processing.

```text
storage/
├── AW100/
├── AW200/
└── preview/
```

**`test/`**

Contains scripts used to test individual project functions.

---

# 🪟 Windows Installation

Windows can be used for local development and testing.

## 1. Clone the repository

Open PowerShell, CMD, or Git Bash:

```bash
git clone https://github.com/cecidavi/Music_Robot_AMR_KUKA.git
cd Music_Robot_AMR_KUKA
```

The following commands should be executed from the project root directory.

---

## 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Once activated, the terminal should look similar to:

```text
(.venv) PS C:\path\Music_Robot_AMR_KUKA>
```

---

## 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

---

# 🎵 Installing FFmpeg on Windows

The application uses **FFmpeg** and **FFprobe** to process audio files.

After downloading and extracting FFmpeg, the directory structure should look similar to:

```text
C:\ffmpeg\
└── bin\
    ├── ffmpeg.exe
    └── ffprobe.exe
```

There are two ways to make FFmpeg available to the application.

---

## Option 1: Add FFmpeg to PATH

Add the FFmpeg `bin` directory to the Windows `PATH`.

For example:

```text
C:\ffmpeg\bin
```

After modifying the `PATH`, close and reopen PowerShell.

Verify the installation:

```powershell
ffmpeg -version
ffprobe -version
```

If both commands are successfully recognized, FFmpeg is correctly configured.

---

## Option 2: Use a specific FFmpeg path

FFmpeg can also be located in a specific directory.

For example:

```text
C:\Programas\KUKA\musicdowload\ffmpeg-9.0.1-
