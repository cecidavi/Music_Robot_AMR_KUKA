from flask import Flask, redirect, render_template, request, send_from_directory, url_for, jsonify
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

@app.route("/audio/source")
def audio_source():
    return send_from_directory(
        "storage/preview",
        "source.mp3",
        mimetype="audio/mpeg"
                 )   


@app.route("/audio/recortado")
def audio_recortado():

    return send_from_directory(
        "storage/preview",
        "source_recortado.mp3",
        mimetype="audio/mpeg"
    )

#prueba de recorte 

@app.route(
    "/recortar",
    methods=["POST"]
)
def recortar_audio():

    inicio = request.form.get(
        "inicio"
    )

    fin = request.form.get(
        "fin"
    )


    print(
        "POST /recortar recibido"
    )

    print(
        "Inicio recibido:",
        inicio
    )

    print(
        "Fin recibido:",
        fin
    )


    resultado = audio.procesar_recorte(
        inicio,
        fin
    )


    if resultado["estado"] == "error":

        return jsonify(
            resultado
        ), 400


    return jsonify(
        resultado
    )



if __name__ == "__main__":

    app.run(
        debug=True
    )