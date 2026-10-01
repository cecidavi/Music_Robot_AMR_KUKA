# services/youtube_service.py

from pathlib import Path
from yt_dlp import YoutubeDL
import yt_dlp
import time

from services.ffmpeg_service import FFmpegService


class YoutubeService:


    def __init__(self):

        self.preview_dir = Path("storage/preview")

        self.preview_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    def obtener_info(self, url):

        opciones = {
            "quiet": True,
            "skip_download": True
        }

        with YoutubeDL(opciones) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

            return {
                "titulo": info.get("title"),
                "duracion": info.get("duration"),
                "canal": info.get("uploader"),
                "thumbnail": info.get("thumbnail")
            }


    # este metodo es para descargar el audio del video de youtube
    def descargar_audio(self, url):

        # Detectar la ubicación de ffmpeg y ffprobe 
        #si tu tienes tu ffmpeg en otra ruta cambia la ruta en ffmpeg_service.py
        #igualmente si tiene en el path de tu sistema operativo no es necesario que hagas nada
        ffmpeg_info = FFmpegService.detectar_ffmpeg()

        ffmpeg_dir = str(
            Path(ffmpeg_info["ffmpeg"]).parent
        )

        #guardo el audio en la carpeta preview y lo renombro como source
        #para asi tener un nombre estandarizado y no tener que estar cambiando 
        #el nombre del archivo cada vez que se descarga un audio
        opciones = {
            "format": "bestaudio/best",

            "outtmpl": str(
                self.preview_dir / "source.%(ext)s"
            ),

            "ffmpeg_location": ffmpeg_dir,

            # reintentos internos de yt-dlp
            # si ocurre un error durante la descarga yt-dlp
            # intentara nuevamente antes de darla por fallida
            "retries": 5,

            # hace lo mismo pero especificamente
            # para los fragmentos de una descarga
            "fragment_retries": 5,

            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }],
        }

        # cantidad maxima de veces que nuestra aplicacion
        # intentara ejecutar nuevamente toda la descarga
        # esto es independiente de los reintentos internos de yt-dlp
        intentos_maximos = 3

        # range genera los intentos:
        # 1, 2 y 3
        for intento in range(
            1,
            intentos_maximos + 1
        ):

            try:

                print(
                    f"Intento de descarga "
                    f"{intento}/{intentos_maximos}"
                )

                # intentamos descargar normalmente
                # exactamente igual que antes
                with yt_dlp.YoutubeDL(opciones) as ydl:

                    ydl.download([url])

                # si llegamos hasta aqui significa
                # que yt-dlp termino la descarga correctamente
                print(
                    "Descarga completada correctamente"
                )

                # terminamos la funcion y ya no hacemos
                # los siguientes intentos
                return True


            except yt_dlp.utils.DownloadError as error:

                # si yt-dlp da un error, por ejemplo
                # HTTP Error 403: Forbidden,
                # entramos a esta parte
                print(
                    f"Error en intento "
                    f"{intento}/{intentos_maximos}: "
                    f"{error}"
                )

                # si ya llegamos al ultimo intento
                # dejamos que el error continue
                if intento == intentos_maximos:
                    raise

                # esperamos un poco antes de volver
 