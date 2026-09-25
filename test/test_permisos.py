#test/test_permisos.py

from services.ssh_service import SSHService


IP = "10.97.65.66"
USUARIO = "kuka"
PASSWORD = "68kuka1secpw59"


ssh = SSHService(
    host=IP,
    usuario=USUARIO,
    password=PASSWORD
)


try:

    print("Conectando al robot...")

    ssh.conectar()

    print("SSH conectado correctamente")


    print("\nPreparando permisos AW100 y AW200...")

    ssh.ejecutar_chown()

    print("Permisos preparados correctamente")


    print("\nAbriendo SFTP...")

    ssh.conectar_stfp()

    print("SFTP conectado correctamente")


    print("\nAW100")
    print("-" * 50)

    archivos = ssh.listar_carpetas(
        "/home/kuka/userdata/kuka_audio/AW100"
    )

    for archivo in archivos:

        print(
            archivo["nombre"],
            archivo["tamano"],
            "bytes",
            "permisos:",
            archivo["permisos"]
        )


    print("\nAW200")
    print("-" * 50)

    archivos = ssh.listar_carpetas(
        "/home/kuka/userdata/kuka_audio/AW200"
    )

    for archivo in archivos:

        print(
            archivo["nombre"],
            archivo["tamano"],
            "bytes",
            "permisos:",
            archivo["permisos"]
        )


finally:

    ssh.cerrar()

    print("\nConexiones cerradas")