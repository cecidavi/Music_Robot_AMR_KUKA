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

#prueba de recorte 

@app.route("/recortar", methods=["POST"])
def recortar_audio():

    inicio = request.form.get("inicio")
    fin = request.form.get("fin")

    print("POST /recortar recibido")
    print("Inicio recibido:", inicio)
    print("Fin recibido:", fin)


    if not inicio or not fin:

        return jsonify({
            "estado": "error",
            "mensaje": (
                "No se recibieron los tiempos "
                "de inicio y final."
            )
        }), 400


    inicio = float(inicio)
    fin = float(fin)


    if fin <= inicio:

        return jsonify({
            "estado": "error",
            "mensaje": (
                "El tiempo final debe ser "
                "mayor que el tiempo inicial."
            )
        }), 400


    return jsonify({
        "estado": "correcto",
        "mensaje": (
            "Selección recibida correctamente. "
            f"Inicio: {inicio:.3f} segundos. "
            f"Final: {fin:.3f} segundos."
        ),
        "inicio": inicio,
        "fin": fin,
        "duracion": fin - inicio
    })





if __name__ == "__main__":

    app.run(
        debug=True
    )