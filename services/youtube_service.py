# services/youtube_service.py

from pathlib import Path
from yt_dlp import YoutubeDL
import yt_dlp
from services.ffmpeg_service import FFmpegService
from pathlib import Path


class YoutubeService:



    def __init__(self):
        self.output_dir = Path("storage/original")
        self.output_dir.mkdir(parents=True, exist_ok=True)

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
    #si quieres degar el nomnbre original quita la variable nombre_archivo
    #                               ||||||
    #                               vvvvvv
    def descargar_audio(self, url,nombre_archivo):

        # Detectar la ubicación de ffmpeg y ffprobe 
        #si tu tienes tu ffmpeg en otra ruta cambia la ruta en ffmpeg_service.py
        #igualmente si tiene en el path de tu sistema operativo no es necesario que hagas nada
        ffmpeg_info = FFmpegService.detectar_ffmpeg()

        ffpeg_dir = str(Path(ffmpeg_info["ffmpeg"]).parent)

        opciones = {
            "format": "bestaudio/best",
            # "outtmpl": str(self.output_dir / "%(title)s.%(ext)s"),
            # si quieres el nombre del archivo original descomenta esta linea y comenta la de abajo
            "outtmpl": str(self.output_dir / nombre_archivo),

            "ffmpeg_location": ffpeg_dir,

            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }],
        }
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])