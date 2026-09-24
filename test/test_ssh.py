from services.ssh_service import SSHService


IP = "10.97.66.225"
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


    print("Abriendo SFTP...")

    ssh.conectar_stfp()

    print("SFTP conectado correctamente")


    print("\nAW100")
    print("-" * 50)

    archivos_aw100 = ssh.listar_carpetas(
        "/home/kuka/userdata/kuka_audio/AW100"
    )

    for archivo in archivos_aw100:

        print(
            archivo["nombre"],
            archivo["tamano"],
            "bytes",
            "permisos:",
            archivo["permisos"]
        )


    print("\nAW200")
    print("-" * 50)

    archivos_aw200 = ssh.listar_carpetas(
        "/home/kuka/userdata/kuka_audio/AW200"
    )

    for archivo in archivos_aw200:

        print(
            archivo["nombre"],
            archivo["tamano"],
            "bytes",
            "permisos:",
            archivo["permisos"]
        )


finally:

    ssh.cerrar()

    print("\nConexión cerrada")