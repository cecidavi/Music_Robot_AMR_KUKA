import paramiko
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, jsonify
from services.audio_service import AudioService
from services.ssh_service import SSHService


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

# ======================================================
# SUBIR ARCHIVOS AL ROBOT
# ======================================================

@app.post("/subir-robot")
def subir_archivos_robot():

    datos = request.get_json(
        silent=True
    ) or {}

    robot_ip = str(
        datos.get("ip", "")
    ).strip()

    if not robot_ip:
        return jsonify({
            "ok": False,
            "error": (
                "No se recibió la dirección IP "
                "del robot."
            )
        }), 400

    robot_usuario = "kuka"
    robot_password = "68kuka1secpw59"

    servicio_ssh = SSHService(
        host=robot_ip,
        usuario=robot_usuario,
        password=robot_password
    )

    try:

        print(
            f"Conectando con el robot {robot_ip}..."
        )

        servicio_ssh.conectar()

        print(
            "Preparando permisos de AW100 y AW200..."
        )

        servicio_ssh.ejecutar_chown()

        print(
            "Abriendo conexión SFTP..."
        )

        servicio_ssh.conectar_sftp()

        print(
            "Subiendo los cuatro archivos..."
        )

        resultados = (
            servicio_ssh.subir_archivos_robot()
        )

        print(
            "Los cuatro archivos fueron "
            "subidos y verificados."
        )

        return jsonify({
            "ok": True,
            "mensaje": (
                "Los cuatro archivos se subieron "
                f"y verificaron en el robot {robot_ip}."
            ),
            "archivos": resultados
        })

    except FileNotFoundError as error:

        return jsonify({
            "ok": False,
            "error": str(error)
        }), 404

    except paramiko.AuthenticationException:

        return jsonify({
            "ok": False,
            "error": (
                "El robot rechazó el usuario "
                "o la contraseña."
            )
        }), 401

    except paramiko.SSHException as error:

        return jsonify({
            "ok": False,
            "error": (
                "No fue posible establecer la "
                f"conexión SSH: {error}"
            )
        }), 502

    except TimeoutError:

        return jsonify({
            "ok": False,
            "error": (
                "Se agotó el tiempo intentando "
                f"conectar con {robot_ip}."
            )
        }), 504

    except Exception as error:

        print(
            "Error durante la subida:",
            repr(error)
        )

        return jsonify({
            "ok": False,
            "error": (
                "Error durante la subida: "
                f"{error}"
            )
        }), 500

    finally:

        servicio_ssh.cerrar()

        print(
            "Conexión SSH/SFTP cerrada."
        )



if __name__ == "__main__":
    
    app.run(
        debug=True
    )