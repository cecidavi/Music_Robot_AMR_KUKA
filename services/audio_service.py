from yt_dlp.utils import DownloadError

from services.youtube_service import YoutubeService
from services.ffmpeg_service import FFmpegService


class AudioService:


    def __init__(self):

        self.youtube = YoutubeService()


    # valida que el usuario haya ingresado
    # una URL antes de intentar procesarla
    def validar_url(self, url):

        if not url:

            return (
                "Debes ingresar una URL de YouTube."
            )

        # valida que el usuario haya pegado una URL
        # y no solamente el nombre de una cancion
        if not (
            url.startswith("http://")
            or url.startswith("https://")
        ):

            return (
                "Debes pegar la URL del video de YouTube. "
                "No escribas solamente el nombre de la canción."
            )

        return None


    # este metodo controla todo el proceso
    # desde la URL hasta generar los archivos
    # necesarios para los robots
    def procesar_audio(self, url):

        error = self.validar_url(url)

        if error:

            return {
                "exito": False,
                "mensaje": None,
                "error": error,
                "info": None
            }

        try:

            # obtenemos la informacion del video
            # antes de descargar el audio
            info = self.youtube.obtener_info(url)

            # descargamos el audio del video
            self.youtube.descargar_audio(url)

            # generamos los archivos necesarios
            # para los robots KUKA
            FFmpegService.generar_archivos_robot()

            return {
                "exito": True,
                "mensaje": "Archivos generados correctamente",
                "error": None,
                "info": info
            }


        except DownloadError as excepcion:

            print(
                f"Error de yt-dlp: {excepcion}"
            )

            return {
                "exito": False,
                "mensaje": None,
                "error": (
                    "No fue posible obtener o descargar "
                    "el video de YouTube."
                ),
                "info": None
            }


        except Exception as excepcion:

            print(
                f"Error inesperado: {excepcion}"
            )

            return {
                "exito": False,
                "mensaje": None,
                "error": (
                    "Ocurrió un error al procesar el video."
                ),
                "info": None
            }
    def procesar_recorte(
        self,
        inicio,
        fin
    ):

        try:

            inicio = float(inicio)
            fin = float(fin)


            archivo_recortado = (
                FFmpegService.recortar_source(
                    inicio,
                    fin
                )
            )


            FFmpegService.generar_archivos_robot(
                archivo_recortado
            )


            return {
                "estado": "correcto",

                "mensaje": (
                    "Recorte completo. "
                    "Los archivos AW100 y AW200 "
                    "fueron regenerados."
                ),

                "inicio": inicio,

                "fin": fin,

                "duracion": fin - inicio,

                "archivo_recortado": True
            }


        except Exception as error:

            print(
                "Error procesando recorte:",
                error
            )


            return {
                "estado": "error",

                "mensaje": str(error),

                "archivo_recortado": False
            }


