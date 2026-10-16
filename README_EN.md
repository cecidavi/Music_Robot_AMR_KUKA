# 🎵 Music Robot AMR KUKA

[🇲🇽 Leer en Español](README.md)

Web application developed with **Python and Flask** to manage, process, and replace audio files used by **KUKA AMRs**.

The application allows users to download audio, preview it, optionally trim it, convert it to the formats used by the robot, and transfer the resulting files directly to the AMR using **SSH/SFTP**.

---

## 📌 Project Objective

Simplify the process of changing music and sound files on KUKA AMRs.

Instead of manually downloading, editing, converting, and transferring each audio file, the application centralizes these operations in a web interface.

---

## 🚀 Features

The application can:

- Download audio files.
- Generate a source file for processing.
- Preview and play audio.
- Select a specific section of the audio.
- Optionally trim an audio file.
- Use the complete audio file without trimming.
- Process audio using FFmpeg.
- Generate the required AW100 and AW200 files.
- Receive the robot IP address through the web interface.
- Establish an SSH connection with the AMR.
- Transfer files using SFTP.
- Run locally on Windows.
- Run locally on Linux.
- Be deployed with Docker on a Linux server.

---

## 🔄 General Workflow

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
 Trim       Full audio
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

## 🛠️ Technologies

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
│   ├── AW100/
│   ├── AW200/
│   └── preview/
├── templates/
└── test/
```

### Main directories

- **`models/`**: contains the models used by the application.
- **`services/`**: contains the download, audio processing, and robot communication logic.
- **`templates/`**: contains the HTML pages used by Flask.
- **`static/`**: contains CSS, JavaScript, and other static resources.
- **`storage/`**: contains the source, preview, AW100, and AW200 audio files.
- **`test/`**: contains scripts used to test individual project functions.

---

## ✅ Requirements

Before running the application, the following components are required:

- Python 3
- pip
- Git
- FFmpeg and FFprobe
- Network access to the KUKA AMRs
- Docker and Docker Compose, only when running the application in containers

Verify that the main tools are installed:

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

> **Note:** The computer or server running the application must have network connectivity to the KUKA AMRs in order to transfer files using SSH/SFTP.

---

# 🪟 Windows Installation and Execution

This option is mainly recommended for local development and testing.

## 1. Clone the Repository

Open PowerShell, CMD, or Git Bash and run:

```bash
git clone https://github.com/cecidavi/Music_Robot_AMR_KUKA.git
cd Music_Robot_AMR_KUKA
```

---

## 2. Create a Virtual Environment

From the project root directory:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Once activated, the terminal should look similar to:

```text
(.venv) PS C:\Programas\KUKA\python\Music_Robot_AMR_KUKA>
```

> If PowerShell blocks virtual environment activation, it can be temporarily enabled for the current session:
>
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .venv\Scripts\Activate.ps1
> ```

---

## 3. Install Python Dependencies

With the virtual environment activated:

```powershell
pip install -r requirements.txt
```

---

## 4. Install FFmpeg on Windows

FFmpeg must be installed on Windows so the application can convert and process audio files.

After downloading and extracting FFmpeg, the directory structure should look similar to:

```text
C:\ffmpeg\
└── bin\
    ├── ffmpeg.exe
    └── ffprobe.exe
```

The `bin` directory should be added to the Windows `PATH` environment variable.

For example:

```text
C:\ffmpeg\bin
```

### Verify the installation

After modifying the `PATH`, close and reopen PowerShell.

Run:

```powershell
ffmpeg -version
ffprobe -version
```

If both commands display version information, FFmpeg is correctly configured.

### Alternative: use a specific FFmpeg path

If FFmpeg is not added to the `PATH`, the project can be configured to use the executable locations directly.

Example:

```text
C:\Programas\KUKA\musicdowload\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe
```

FFprobe path:

```text
C:\Programas\KUKA\musicdowload\ffmpeg-9.0.1-essentials_build\bin\ffprobe.exe
```

In this case, the application must use those paths when executing FFmpeg or FFprobe.

> Adding FFmpeg to the `PATH` is recommended because it prevents the project from depending on a specific location on one computer.

---

## 5. Run the Application on Windows

From the project root directory and with `.venv` activated:

```powershell
python App.py
```

The Flask application will start using the configuration defined in `App.py`.

To stop it:

```text
Ctrl + C
```

---

# 🐧 Linux Installation and Execution

The application can also run on a Linux computer or server.

All of the following commands should be executed from a terminal.

## 1. Clone the Project

```bash
cd ~
git clone https://github.com/cecidavi/Music_Robot_AMR_KUKA.git
cd Music_Robot_AMR_KUKA
```

The terminal should now be located inside:

```text
~/Music_Robot_AMR_KUKA
```

Verify the current location:

```bash
pwd
```

Check the project files:

```bash
ls
```

Files and directories such as the following should be available:

```text
App.py
Dockerfile
compose.yaml
gunicorn.conf.py
requirements.txt
models
services
static
storage
templates
test
```

---

## 2. Install System Dependencies

On Ubuntu or Debian-based systems:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv ffmpeg
```

Verify the installations:

```bash
python3 --version
pip3 --version
ffmpeg -version
ffprobe -version
```

---

# 🐧 Running Directly on Linux

To run the application without Docker, create a virtual environment first.

Navigate to the project root:

```bash
cd ~/Music_Robot_AMR_KUKA
```

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

For development or testing:

```bash
python App.py
```

To stop the application:

```text
Ctrl + C
```

To exit the virtual environment:

```bash
deactivate
```

---

# 🐳 Running on Linux with Docker

Docker is recommended when running the application on a Linux server.

Before executing Docker Compose commands, navigate to the project root:

```bash
cd ~/Music_Robot_AMR_KUKA
```

The structure should contain at least:

```text
Music_Robot_AMR_KUKA/
├── App.py
├── Dockerfile
├── compose.yaml
├── gunicorn.conf.py
├── requirements.txt
├── services/
├── static/
├── storage/
└── templates/
```

The `compose.yaml` file must be in the directory where the Docker Compose commands are executed.

---

## Build the Image

```bash
docker compose build
```

---

## Start the Application

```bash
docker compose up -d
```

The `-d` option starts the containers in the background.

---

## Verify the Running Container

```bash
docker ps
```

The project status can also be checked with:

```bash
docker compose ps
```

---

## View the Logs

Show the latest 100 log entries:

```bash
docker compose logs --tail=100
```

Follow the logs in real time:

```bash
docker compose logs -f
```

Exit the log view without stopping the container:

```text
Ctrl + C
```

---

## Stop the Application

```bash
docker compose down
```

---

## Restart the Application

```bash
docker compose restart
```

---

## Rebuild After Changes

If the code, `Dockerfile`, or Python dependencies have changed:

```bash
docker compose down
docker compose up -d --build
```

It can also be rebuilt directly with:

```bash
docker compose up -d --build
```

---

## 🔄 Update the Project on the Server

If the project is already cloned and new changes are available:

```bash
cd ~/Music_Robot_AMR_KUKA
git pull
```

Rebuild the container:

```bash
docker compose up -d --build
```

Verify its status:

```bash
docker ps
```

If necessary, check the logs:

```bash
docker compose logs --tail=100
```

---

# 📦 Managing Python Dependencies

When a new dependency is installed during development:

```bash
pip install package_name
```

Update the following file:

```text
requirements.txt
```

For example:

```bash
pip freeze > requirements.txt
```

Commit and push the changes:

```bash
git add requirements.txt
git commit -m "Update dependencies"
git push
```

On the server, retrieve the changes and rebuild the image:

```bash
cd ~/Music_Robot_AMR_KUKA
git pull
docker compose up -d --build
```

---

# 🎧 Audio Processing

The application uses FFmpeg to process and convert audio files before transferring them to the robot.

```text
Downloaded audio
       ↓
   source.mp3
       ↓
     Preview
       ↓
 Trim audio?
   ↓         ↓
  Yes        No
   ↓         ↓
 Trim      Full audio
    \        /
     ↓      ↓
 FFmpeg processing
       ↓
    AMR files
    ↓       ↓
 AW100    AW200
```

---

# 📂 Generated Files

Example of the files generated by the application:

```text
storage/
│
├── preview/
│   └── source.mp3
│
├── AW100/
│   ├── 0100.mp3
│   └── 100.wav
│
└── AW200/
    ├── 0200.mp3
    └── 200.wav
```

- `preview/` contains the audio used for preview and selection.
- `AW100/` contains files prepared for AW100.
- `AW200/` contains files prepared for AW200.

---

# 🔌 Checking AMR Connectivity

The computer running the application must be able to communicate with the robot network.

## Windows

```powershell
ping <ROBOT_IP>
```

## Linux

```bash
ping <ROBOT_IP>
```

For example:

```bash
ping 10.x.x.x
```

The application will use the provided IP address to establish the connection with the AMR and transfer the files.

If the application runs inside Docker, the container environment must also have connectivity to the robot network.

---

# 🗂️ Where Should Each Command Be Run?

## Windows

Navigate to the project:

```powershell
cd C:\path\to\Music_Robot_AMR_KUKA
```

Activate the environment and run the application:

```powershell
.venv\Scripts\Activate.ps1
python App.py
```

## Linux without Docker

Navigate to the project:

```bash
cd ~/Music_Robot_AMR_KUKA
```

Activate the environment and run the application:

```bash
source .venv/bin/activate
python App.py
```

## Linux with Docker

Navigate to the project:

```bash
cd ~/Music_Robot_AMR_KUKA
```

Run the Docker commands:

```bash
docker compose build
docker compose up -d
docker compose logs -f
docker compose down
```

> `docker compose` commands should be executed from the directory containing `compose.yaml`.

---

# 🧪 Testing

Test scripts are located inside:

```text
test/
```

These scripts can be used to individually verify functions such as:

- SSH connectivity.
- AMR communication.
- Audio processing.
- File generation.
- SFTP transfers.

---

# 🐛 Troubleshooting

## FFmpeg is not recognized as a command

Verify that the FFmpeg `bin` directory is included in the Windows `PATH`.

Example:

```text
C:\ffmpeg\bin
```

Close and reopen PowerShell:

```powershell
ffmpeg -version
ffprobe -version
```

---

## Docker Compose cannot find the configuration file

Navigate to the project root:

```bash
cd ~/Music_Robot_AMR_KUKA
```

Verify the project files:

```bash
ls
```

The following file should be available:

```text
compose.yaml
```

Then run:

```bash
docker compose ps
```

---

## The Application Cannot Communicate with the AMR

Check network connectivity:

```bash
ping <ROBOT_IP>
```

Also verify that the entered IP address belongs to the correct robot.

---

## Docker Cannot Find a New Dependency

Verify that the dependency is listed in:

```text
requirements.txt
```

Then rebuild the image:

```bash
docker compose up -d --build
```

---

# ⚠️ Considerations

- Always verify the robot IP address before transferring files.
- The computer running the application must have access to the AMR network.
- FFmpeg and FFprobe must be available for audio processing.
- Files inside `storage/` may be modified while the application is running.
- A `.venv` virtual environment is recommended on Windows.
- Docker is recommended for deployment on a Linux server.
- Audio changes should only be performed on authorized robots.

---

# 📝 Project Status

This project is currently under development.

Its objective is to simplify and automate the management of music and sound files on AMRs, reducing the manual operations required to prepare and transfer audio files.

---

# 👤 Author

**Cecilio Sanchez**  
IoT Controls Engineer

---

[🇲🇽 Leer esta documentación en Español](README.md)