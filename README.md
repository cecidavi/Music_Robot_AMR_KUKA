## ✅ Requisitos

Antes de ejecutar la aplicación se necesita:

- Python 3
- pip
- Git
- FFmpeg y FFprobe
- Acceso de red a los robots KUKA AMR
- Docker y Docker Compose (únicamente si se ejecutará mediante contenedores)

Para comprobar que las herramientas principales están instaladas:

```bash
python --version
pip --version
ffmpeg -version
ffprobe -version
```

> **Nota:** El equipo donde se ejecute la aplicación debe tener conectividad de red con los AMR KUKA para poder realizar la transferencia de archivos mediante SSH/SFTP.

---

# 🪟 Instalación y ejecución en Windows

Esta opción se recomienda principalmente para desarrollo y pruebas locales.

## 1. Clonar el repositorio

Abrir PowerShell, CMD o Git Bash y ejecutar:

```bash
git clone <URL_DEL_REPOSITORIO>
cd Music_Robot_AMR_KUKA
```

---

## 2. Crear el entorno virtual

Desde la raíz del proyecto:

```powershell
python -m venv .venv
```

Activarlo en PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Una vez activado aparecerá algo similar a:

```text
(.venv) PS C:\Programas\KUKA\python\Music_Robot_AMR_KUKA>
```

---

## 3. Instalar las dependencias

Con el entorno virtual activado:

```powershell
pip install -r requirements.txt
```

---

## 4. Instalar FFmpeg en Windows

FFmpeg debe estar instalado en Windows para que la aplicación pueda convertir y procesar los archivos de audio.

Después de descargar y descomprimir FFmpeg, se tendrá una estructura similar a:

```text
C:\ffmpeg\
└── bin\
    ├── ffmpeg.exe
    └── ffprobe.exe
```

La carpeta `bin` debe agregarse a la variable de entorno `PATH` de Windows.

Por ejemplo:

```text
C:\ffmpeg\bin
```

### Comprobar la instalación

Cerrar y volver a abrir PowerShell y ejecutar:

```powershell
ffmpeg -version
ffprobe -version
```

Si ambos comandos muestran información de versión, FFmpeg está correctamente configurado.

### Alternativa: usar una ruta específica

Si no se desea agregar FFmpeg al `PATH`, el proyecto también puede configurarse para utilizar directamente la ubicación de los ejecutables.

Ejemplo:

```text
C:\Programas\KUKA\musicdowload\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe
```

y:

```text
C:\Programas\KUKA\musicdowload\ffmpeg-9.0.1-essentials_build\bin\ffprobe.exe
```

En este caso, la aplicación deberá utilizar esas rutas al ejecutar FFmpeg o FFprobe.

> Se recomienda utilizar `PATH`, ya que evita depender de una ubicación específica de FFmpeg dentro de una computadora.

---

## 5. Ejecutar la aplicación en Windows

Desde la raíz del proyecto:

```text
Music_Robot_AMR_KUKA/
```

y con `.venv` activado:

```powershell
python App.py
```

La aplicación Flask iniciará utilizando la configuración definida en `App.py`.

Para detenerla:

```text
Ctrl + C
```

---

# 🐧 Instalación y ejecución en Linux

La aplicación también puede ejecutarse en un servidor Linux.

Todos los siguientes comandos deben ejecutarse desde una terminal.

## 1. Clonar el proyecto

```bash
cd ~
git clone <URL_DEL_REPOSITORIO>
cd Music_Robot_AMR_KUKA
```

La terminal deberá quedar ubicada dentro de:

```text
~/Music_Robot_AMR_KUKA
```

Se puede comprobar con:

```bash
pwd
```

y:

```bash
ls
```

Deberán aparecer archivos como:

```text
App.py
Dockerfile
compose.yaml
gunicorn.conf.py
requirements.txt
services
static
storage
templates
```

---

## 2. Instalar dependencias del sistema

En sistemas basados en Ubuntu o Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv ffmpeg
```

Comprobar FFmpeg:

```bash
ffmpeg -version
ffprobe -version
```

---

# 🐧 Ejecución directa en Linux

Si se desea ejecutar la aplicación sin Docker, primero se crea un entorno virtual.

Desde:

```text
~/Music_Robot_AMR_KUKA
```

ejecutar:

```bash
python3 -m venv .venv
```

Activarlo:

```bash
source .venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Para desarrollo o pruebas:

```bash
python App.py
```

---

# 🐳 Ejecución en Linux con Docker

Para el servidor se recomienda utilizar Docker.

Primero entrar a la raíz del proyecto:

```bash
cd ~/Music_Robot_AMR_KUKA
```

La estructura debe contener como mínimo:

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

## Construir la imagen

```bash
docker compose build
```

---

## Iniciar la aplicación

```bash
docker compose up -d
```

---

## Verificar que el contenedor esté funcionando

```bash
docker ps
```

---

## Ver los logs

```bash
docker compose logs --tail=100
```

Para observar los logs en tiempo real:

```bash
docker compose logs -f
```

Para salir de los logs sin detener el contenedor:

```text
Ctrl + C
```

---

## Detener la aplicación

```bash
docker compose down
```

---

## Reconstruir después de realizar cambios

Si se modificó el código o se agregaron nuevas dependencias:

```bash
docker compose down
docker compose up -d --build
```

También puede utilizarse directamente:

```bash
docker compose up -d --build
```

---

## 🔄 Actualizar el proyecto en el servidor

Si el proyecto ya está clonado y existen cambios nuevos en el repositorio:

```bash
cd ~/Music_Robot_AMR_KUKA
git pull
```

Después se puede reconstruir el contenedor:

```bash
docker compose up -d --build
```

Finalmente:

```bash
docker ps
```

y, si es necesario:

```bash
docker compose logs --tail=100
```

---

# 📦 Administración de dependencias de Python

Cuando durante el desarrollo se instala una nueva dependencia:

```bash
pip install nombre_paquete
```

se debe actualizar:

```text
requirements.txt
```

Por ejemplo:

```bash
pip freeze > requirements.txt
```

Después de subir los cambios al repositorio, el servidor deberá reconstruir la imagen Docker para instalar las nuevas dependencias:

```bash
docker compose up -d --build
```

---

# 🔌 Verificación de conectividad con los AMR

El equipo que ejecuta la aplicación debe poder comunicarse con la red de los robots.

En Linux puede comprobarse inicialmente con:

```bash
ping <IP_ROBOT>
```

Por ejemplo:

```bash
ping 10.x.x.x
```

La aplicación utilizará posteriormente la IP proporcionada para establecer la conexión necesaria con el AMR y transferir los archivos.

Si la aplicación funciona dentro de Docker, es importante verificar que la conectividad hacia el robot también exista desde el entorno donde se ejecuta el contenedor.

---

# 🗂️ ¿Dónde ejecutar cada comando?

Una regla sencilla para trabajar con el proyecto:

### Windows

Primero:

```powershell
cd C:\ruta\al\proyecto\Music_Robot_AMR_KUKA
```

Después ejecutar los comandos relacionados con Python:

```powershell
.venv\Scripts\Activate.ps1
python App.py
```

### Linux

Primero:

```bash
cd ~/Music_Robot_AMR_KUKA
```

Después ejecutar los comandos de Docker:

```bash
docker compose build
docker compose up -d
docker compose logs -f
docker compose down
```

El archivo `compose.yaml` se encuentra en la raíz del proyecto, por lo que los comandos de `docker compose` deben ejecutarse desde esa ubicación.
