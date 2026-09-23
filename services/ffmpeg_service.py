#services/ffmpeg_service.py

import shutil
from pathlib import Path
import platform
import subprocess


class FFmpegService:

    @staticmethod
    def detectar_ffmpeg():
    

        ffmpeg = shutil.which("ffmpeg")
        ffprobe = shutil.which("ffprobe")

        if ffmpeg and ffprobe:
            return {
                "sistema": platform.system(),
                "ffmpeg": ffmpeg,
                "ffprobe": ffprobe
            }

        # Desarrollo local Windows
        #por temas de seguridad y permisos no puedo instalar ffmpeg en el path de mi sistema operativo
        #pero lo podemos mandar a llmar desde la ruta donde lo tenemos guardado
        #si tu tienes tu ffmpeg en otra ruta cambia la ruta en ffmpeg_service.py
        #si lo tienes en el path de tu sistema operativo no es necesario que hagas nada
        #te recomiendo guardarla en el path si te es posible
        #si no es buena idea dejarlo en una carpeta de tu proyecto y llamarlo desde ahi
        #oh simpelmente en una ubicacion comoda
        #nota esto es para windows si usas linux es de otra forma
        ffmpeg = Path(
            r"C:\Programas\KUKA\musicdowload\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe"
        )

        ffprobe = Path(
            r"C:\Programas\KUKA\musicdowload\ffmpeg-9.0.1-essentials_build\bin\ffprobe.exe"
        )

        if ffmpeg.exists() and ffprobe.exists():
            return {
                "sistema": platform.system(),
                "ffmpeg": str(ffmpeg),
                "ffprobe": str(ffprobe)
            }

        raise Exception(
            "ffmpeg o ffprobe no fueron encontrados"
        )



       
    @staticmethod
    def convertir_mp3_wav(
        archivo_entrada,
        archivo_salida
    ):

        info = FFmpegService.detectar_ffmpeg()

        ffmpeg = info["ffmpeg"]

        comando = [
            ffmpeg,
            "-y",
            "-i",
            archivo_entrada,
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "2",
            archivo_salida
        ]

        subprocess.run(
            comando,
            check=True
        )

        return archivo_salida

    @staticmethod
    def generar_archivos_robot():

        source = Path("storage/preview/source.mp3")

        aw100_dir = Path("storage/AW100")
        aw200_dir = Path("storage/AW200")

        aw100_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        aw200_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # Copiar MP3 AW100
        shutil.copy2(
            source,
            aw100_dir / "0100.mp3"
        )

        # Copiar MP3 AW200
        shutil.copy2(
            source,
            aw200_dir / "0200.mp3"
        )

        # Generar WAV AW100
        FFmpegService.convertir_mp3_wav(
            str(aw100_dir / "0100.mp3"),
            str(aw100_dir / "100.wav")
        )

        # Generar WAV AW200
        FFmpegService.convertir_mp3_wav(
            str(aw200_dir / "0200.mp3"),
            str(aw200_dir / "200.wav")
        )

        return True