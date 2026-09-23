#services/ffmpeg_service.py

import shutil
from pathlib import Path
import platform

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