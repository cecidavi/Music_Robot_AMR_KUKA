from pathlib import Path
from yt_dlp import YoutubeDL
import yt_dlp


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


    def descargar_audio(self, url):

        opciones = {
            "format": "bestaudio/best",
            "outtmpl": str(self.output_dir) + "/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }],
        }
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])