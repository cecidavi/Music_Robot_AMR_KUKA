from flask import Flask, render_template, request

from services.youtube_service import YoutubeService
from services.ffmpeg_service import FFmpegService

app = Flask(__name__)

youtube = YoutubeService()


@app.route("/", methods=["GET", "POST"])
def index():

    mensaje = None

    if request.method == "POST":

        url = request.form.get(
            "youtube_url"
        )

        youtube.descargar_audio(url)

        FFmpegService.generar_archivos_robot()

        mensaje = (
            "Archivos generados correctamente"
        )

    return render_template(
        "index.html",
        mensaje=mensaje
    )


if __name__ == "__main__":
    app.run(
        debug=True
    )