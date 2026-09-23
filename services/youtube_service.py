# services/youtube_service.py

from pathlib import Path
from yt_dlp import YoutubeDL
import yt_dlp
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

        ffmpeg_dir = str(Path(ffmpeg_info["ffmpeg"]).parent)

            #guardo el audio en la carpeta preview y lo renombro como source
            #para asi tener un nombre estandarizado y no tener que estar cambiando 
            #el nombre del archivo cada vez que se descarga un audio
            
        opciones = {
            "format": "bestaudio/best",
            "outtmpl": str(self.preview_dir / "source.%(ext)s"),

            "ffmpeg_location": ffmpeg_dir,
    
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }],
        }
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])