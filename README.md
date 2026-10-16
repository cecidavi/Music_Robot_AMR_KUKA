# 🎵 Music Robot AMR KUKA

[🇺🇸 Read in English](README_EN.md)

Aplicación web desarrollada en **Python y Flask** para gestionar, procesar y reemplazar archivos de audio utilizados por robots **KUKA AMR**.

La aplicación permite descargar audio, previsualizarlo, realizar un recorte opcional, convertirlo a los formatos utilizados por el robot y transferir los archivos directamente al AMR mediante **SSH/SFTP**.

---

## 📌 Objetivo del proyecto

Simplificar el proceso de cambio de música y sonidos en los robots KUKA AMR.

En lugar de descargar, editar, convertir y transferir manualmente cada archivo, la aplicación centraliza estas operaciones en una interfaz web.

---

## 🚀 Funcionalidades

La aplicación permite:

- Descargar archivos de audio.
- Generar un archivo fuente para su procesamiento.
- Previsualizar y reproducir el audio.
- Seleccionar una sección del audio.
- Recortar una canción de forma opcional.
- Utilizar la canción completa sin realizar un recorte.
- Procesar archivos mediante FFmpeg.
- Generar los archivos requeridos para AW100 y AW200.
- Ingresar la dirección IP del robot desde la interfaz web.
- Establecer una conexión SSH con el AMR.
- Transferir archivos mediante SFTP.
- Ejecutarse localmente en Windows.
- Ejecutarse localmente en Linux.
- Desplegarse mediante Docker en un servidor Linux.

---

## 🔄 Flujo general

```text
Descargar audio
      ↓
Generar archivo fuente
      ↓
Previsualizar / escuchar
      ↓
¿Se necesita recorte?
   ↓           ↓
  Sí           No
   ↓           ↓
Recortar    Audio completo
      \       /
       ↓     ↓
Procesar audio
       ↓
Generar archivos
AW100 / AW200
       ↓
Ingresar IP del robot
       ↓
Conexión SSH/SFTP
       ↓
Subir archivos al AMR
```

---

## 🛠️ Tecnologías utilizadas

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

## 📁 Estructura del proyecto

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

### Carpetas principales

- **`models/`**: contiene los modelos utilizados por la aplicación.
- **`services/`**: contiene la lógica de descarga, procesamiento de audio y comunicación con los robots.
- **`templates/`**: contiene las páginas HTML utilizadas por Flask.
- **`static/`**: contiene los archivos CSS, JavaScript y otros recursos estáticos.
- **`storage/`**: contiene los archivos fuente, previsualizaciones y archivos generados para AW100 y AW200.
- **`test/`**: contiene scripts para probar individualmente las funciones del proyecto.

---

## ✅ Requisitos

Antes de ejecutar la aplicación se necesita:

- Python 3
- pip
- Git
- FFmpeg y FFprobe
- Acceso de red a los robots KUKA AMR
- Docker y Docker Compose, únicamente si se ejecutará mediante contenedores

Para comprobar que las herramientas principales están instaladas:

```bash
python --version
pip --version
ffmpeg -version
ffprobe -version
```

En Linux puede ser necesario utilizar:

```bash
python3 --version
pip3 --version
```

> **Nota:** El equipo donde se ejecute la aplicación debe tener conectividad de red con los AMR KUKA para poder realizar la transferencia de archivos mediante SSH/SFTP.

---

# 🪟 Instalación y ejecución en Windows

Esta opción se recomienda principalmente para desarrollo y pruebas locales.

## 1. Clonar el repositorio

Abrir PowerShell, CMD o Git Bash y ejecutar:

```bash
git clone https://github.com/cecidavi/Music_Robot_AMR_KUKA.git
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

> Si PowerShell bloquea la activación del entorno virtual, se puede permitir temporalmente para la sesión actual con:
>
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .venv\Scripts\Activate.ps1
> ```

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

Después de modificar el `PATH`, cerrar y volver a abrir PowerShell.

Ejecutar:

```powershell
ffmpeg -version
ffprobe -version
```

Si ambos comandos muestran información de versión, FFmpeg está correctamente configurado.

### Alternativa: utilizar una ruta específica

Si no se desea agregar FFmpeg al `PATH`, el proyecto puede configurarse para utilizar directamente la ubicación de los ejecutables.

Ejemplo:

```text
C:\Programas\KUKA\musicdowload\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe
```

Y para FFprobe:

```text
C:\Programas\KUKA\musicdowload\ffmpeg-9.0.1-essentials_build\bin\ffprobe.exe
```

En este caso, la aplicación debe utilizar esas rutas cuando ejecute FFmpeg o FFprobe.

> Se recomienda utilizar el `PATH`, ya que evita depender de una ubicación específica de FFmpeg dentro de una computadora.

---

## 5. Ejecutar la aplicación en Windows

Desde la raíz del proyecto y con `.venv` activado:

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

La aplicación también puede ejecutarse en una computadora o servidor Linux.

Todos los siguientes comandos deben ejecutarse desde una terminal.

## 1. Clonar el proyecto

```bash
cd ~
git clone https://github.com/cecidavi/Music_Robot_AMR_KUKA.git
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

También se pueden revisar los archivos con:

```bash
ls
```

Deberán aparecer archivos y carpetas como:

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

## 2. Instalar dependencias del sistema

En sistemas basados en Ubuntu o Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv ffmpeg
```

Comprobar las instalaciones:

```bash
python3 --version
pip3 --version
ffmpeg -version
ffprobe -version
```

---

# 🐧 Ejecución directa en Linux

Si se desea ejecutar la aplicación sin Docker, primero se debe crear un entorno virtual.

Entrar a la raíz del proyecto:

```bash
cd ~/Music_Robot_AMR_KUKA
```

Crear el entorno virtual:

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

Para detener la aplicación:

```text
Ctrl + C
```

Para salir del entorno virtual:

```bash
deactivate
```

---

# 🐳 Ejecución en Linux con Docker

Para ejecutar la aplicación en un servidor Linux se recomienda utilizar Docker.

Antes de ejecutar cualquier comando de Docker Compose, entrar a la raíz del proyecto:

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

El archivo `compose.yaml` debe encontrarse en la carpeta desde la cual se ejecutan los comandos de Docker Compose.

---

## Construir la imagen

```bash
docker compose build
```

---

## Iniciar la aplicación

```bash
docker compose up -d
```

La opción `-d` inicia los contenedores en segundo plano.

---

## Verificar que el contenedor esté funcionando

```bash
docker ps
```

También se puede consultar el estado del proyecto con:

```bash
docker compose ps
```

---

## Ver los logs

Mostrar los últimos 100 registros:

```bash
docker compose logs --tail=100
```

Observar los logs en tiempo real:

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

## Reiniciar la aplicación

```bash
docker compose restart
```

---

## Reconstruir después de realizar cambios

Si se modificó el código, el `Dockerfile` o las dependencias:

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

Después, reconstruir el contenedor:

```bash
docker compose up -d --build
```

Verificar su estado:

```bash
docker ps
```

Si es necesario, revisar los logs:

```bash
docker compose logs --tail=100
```

---

# 📦 Administración de dependencias de Python

Cuando durante el desarrollo se instale una nueva dependencia:

```bash
pip install nombre_paquete
```

Se debe actualizar el archivo:

```text
requirements.txt
```

Por ejemplo:

```bash
pip freeze > requirements.txt
```

Después se pueden subir los cambios:

```bash
git add requirements.txt
git commit -m "Actualizar dependencias"
git push
```

En el servidor se deben descargar los cambios y reconstruir la imagen:

```bash
cd ~/Music_Robot_AMR_KUKA
git pull
docker compose up -d --build
```

---

# 🎧 Procesamiento de audio

La aplicación utiliza FFmpeg para procesar y convertir los archivos antes de transferirlos al robot.

```text
Audio descargado
       ↓
   source.mp3
       ↓
Vista previa
       ↓
¿Recortar audio?
   ↓         ↓
  Sí         No
   ↓         ↓
Recorte    Completo
    \        /
     ↓      ↓
Procesamiento FFmpeg
       ↓
  Archivos AMR
    ↓       ↓
 AW100    AW200
```

---

# 📂 Archivos generados

Ejemplo de los archivos generados por la aplicación:

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

- `preview/` contiene el archivo utilizado para previsualizar y trabajar con el audio.
- `AW100/` contiene los archivos preparados para AW100.
- `AW200/` contiene los archivos preparados para AW200.

---

# 🔌 Verificación de conectividad con los AMR

El equipo que ejecuta la aplicación debe poder comunicarse con la red de los robots.

## Windows

```powershell
ping <IP_ROBOT>
```

## Linux

```bash
ping <IP_ROBOT>
```

Por ejemplo:

```bash
ping 10.x.x.x
```

La aplicación utilizará la IP proporcionada para establecer la conexión con el AMR y transferir los archivos.

Si la aplicación funciona dentro de Docker, también debe existir conectividad entre el entorno donde se ejecuta el contenedor y la red del robot.

---

# 🗂️ ¿Dónde ejecutar cada comando?

## Windows

Primero entrar al proyecto:

```powershell
cd C:\ruta\al\proyecto\Music_Robot_AMR_KUKA
```

Después activar el entorno y ejecutar la aplicación:

```powershell
.venv\Scripts\Activate.ps1
python App.py
```

## Linux sin Docker

Primero entrar al proyecto:

```bash
cd ~/Music_Robot_AMR_KUKA
```

Después activar el entorno y ejecutar la aplicación:

```bash
source .venv/bin/activate
python App.py
```

## Linux con Docker

Primero entrar al proyecto:

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

> Los comandos `docker compose` deben ejecutarse desde la ubicación donde se encuentra el archivo `compose.yaml`.

---

# 🧪 Pruebas

Los scripts utilizados para realizar pruebas se encuentran dentro de:

```text
test/
```

Estos scripts permiten probar individualmente funciones como:

- Conectividad SSH.
- Comunicación con el AMR.
- Procesamiento de audio.
- Generación de archivos.
- Transferencia mediante SFTP.

---

# 🐛 Solución de problemas

## FFmpeg no se reconoce como comando

Comprobar que la carpeta `bin` de FFmpeg esté incluida en el `PATH`.

Ejemplo:

```text
C:\ffmpeg\bin
```

Cerrar y volver a abrir PowerShell:

```powershell
ffmpeg -version
ffprobe -version
```

---

## Docker Compose no encuentra el archivo de configuración

Entrar a la raíz del proyecto:

```bash
cd ~/Music_Robot_AMR_KUKA
```

Comprobar que existe el archivo:

```bash
ls
```

Debe aparecer:

```text
compose.yaml
```

Después ejecutar:

```bash
docker compose ps
```

---

## La aplicación no puede comunicarse con el AMR

Comprobar inicialmente la conectividad:

```bash
ping <IP_ROBOT>
```

También se debe verificar que la IP ingresada corresponda al robot correcto.

---

## Docker no encuentra una dependencia nueva

Comprobar que la dependencia aparezca en:

```text
requirements.txt
```

Después reconstruir:

```bash
docker compose up -d --build
```

---

# ⚠️ Consideraciones

- Verificar siempre la IP del robot antes de realizar una transferencia.
- El equipo que ejecuta la aplicación debe tener acceso a la red de los AMR.
- FFmpeg y FFprobe deben estar disponibles para procesar el audio.
- Los archivos dentro de `storage/` pueden modificarse durante el uso de la aplicación.
- En Windows se recomienda utilizar un entorno virtual `.venv`.
- En un servidor Linux se recomienda utilizar Docker.
- Los cambios de audio deben realizarse únicamente en robots autorizados.

---

# 📝 Estado del proyecto

El proyecto se encuentra actualmente en desarrollo.

Su objetivo es simplificar y automatizar la administración de música y sonidos de los AMR, reduciendo las operaciones manuales necesarias para preparar y transferir los archivos.

---

# 👤 Autor

**Cecilio Sanchez**  
Ingeniero en Controles IoT

---

[🇺🇸 Read this documentation in English](README_EN.md)
