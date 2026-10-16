# 🎵 Music Robot AMR KUKA

Aplicación web desarrollada en **Python + Flask** para gestionar y reemplazar archivos de audio utilizados por robots **KUKA AMR**.

El sistema permite descargar audio, preparar los archivos en los formatos utilizados por el robot y transferirlos directamente al AMR mediante **SSH/SFTP**.

---

## 📌 Objetivo del proyecto

Simplificar el proceso de cambio de música y sonidos en los robots KUKA AMR mediante una interfaz web.

En lugar de realizar manualmente todo el proceso de descarga, conversión, preparación y transferencia de archivos, la aplicación centraliza estas operaciones en una sola herramienta.

---

## 🚀 Funcionalidades

Actualmente la aplicación permite:

- Descargar audio.
- Generar una vista previa del audio.
- Reproducir el audio antes de enviarlo al robot.
- Seleccionar y recortar una sección de la canción.
- Utilizar la canción completa sin necesidad de recortarla.
- Convertir el audio a los formatos utilizados por el AMR.
- Generar los archivos correspondientes para **AW100** y **AW200**.
- Ingresar la dirección IP del robot.
- Conectarse al AMR mediante SSH.
- Transferir los archivos generados al robot mediante SFTP.
- Ejecutarse localmente o dentro de un contenedor Docker.

---

## 🔄 Flujo de funcionamiento

El flujo general de la aplicación es:

```text
Descargar audio
      ↓
Generar archivo fuente
      ↓
Vista previa / reproducción
      ↓
¿Se necesita recorte?
   ↓           ↓
  Sí           No
   ↓           ↓
Recortar    Audio completo
      \       /
       ↓     ↓
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

El proyecto utiliza principalmente:

- Python
- Flask
- Gunicorn
- FFmpeg
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
├─
