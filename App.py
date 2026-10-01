from flask import Flask, render_template, request

from services.audio_service import AudioService


app = Flask(__name__)

audio = AudioService()


@app.route("/", methods=["GET", "POST"])
def index():

    mensaje = None
    error = None
    info = None

    if request.method == "POST":

        url = request.form.get(
            "youtube_url",
            ""
        ).strip()

        resultado = audio.procesar_audio(url)

        mensaje = resultado["mensaje"]
        error = resultado["error"]
        info = resultado["info"]

    return render_template(
        "index.html",
        mensaje=mensaje,
        error=error,
        info=info
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )