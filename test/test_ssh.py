import os

from services.ssh_service import SSHService


IP_ROBOT = os.getenv(
    "ROBOT_IP"
)

USUARIO_ROBOT = os.getenv(
    "ROBOT_USUARIO"
)

PASSWORD_ROBOT = os.getenv(
    "ROBOT_PASSWORD"
)


if not IP_ROBOT:

    raise ValueError(
        "Falta la variable ROBOT_IP"
    )


if not USUARIO_ROBOT:

    raise ValueError(
        "Falta la variable ROBOT_USUARIO"
    )


if not PASSWORD_ROBOT:

    raise ValueError(
        "Falta la variable ROBOT_PASSWORD"
    )


ssh = SSHService(
    host=IP_ROBOT,
    usuario=USUARIO_ROBOT,
    password=PASSWORD_ROBOT
)


try:

    print(
        "Conectando al robot..."
    )

    ssh.conectar()

    print(
        "SSH conectado correctamente"
    )


    print(
        "Preparando permisos..."
    )

    ssh.ejecutar_chown()

    print(
        "Permisos preparados correctamente"
    )


    print(
        "Abriendo SFTP..."
    )

    ssh.conectar_sftp()

    print(
        "SFTP conectado correctamente"
    )


    print(
        "Subiendo archivos..."
    )

    resultados = (
        ssh.subir_archivos_robot()
    )


    print(
        "\nArchivos subidos y verificados:"
    )


    for resultado in resultados:

        print(
            resultado["ruta_remota"],
            resultado["tamano_remoto"],
            "bytes",
            "OK"
        )


finally:

    ssh.cerrar()

    print(
        "Conexiones cerradas"
    )