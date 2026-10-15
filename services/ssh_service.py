import paramiko

from pathlib import Path


class SSHService:

    RUTA_BASE_REMOTA = (
        "/home/kuka/userdata/kuka_audio"
    )


    def __init__(
        self,
        host,
        usuario,
        password,
        puerto=22
    ):

        self.host = host
        self.usuario = usuario
        self.password = password
        self.puerto = puerto

        self.cliente = None
        self.sftp = None


    # ==================================================
    # CONEXIÓN SSH
    # ==================================================

    def conectar(self):

        self.cliente = paramiko.SSHClient()

        self.cliente.load_system_host_keys()

        self.cliente.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        self.cliente.connect(
            hostname=self.host,
            port=self.puerto,
            username=self.usuario,
            password=self.password,
            timeout=10,
            allow_agent=False,
            look_for_keys=False
        )

        return True


    # ==================================================
    # EJECUTAR COMANDO CON SUDO
    # ==================================================

    def ejecutar_sudo(self, comando):

        if not self.cliente:

            raise Exception(
                "No hay conexión SSH establecida."
            )


        comando_sudo = (
            f"sudo -S -p '' {comando}"
        )


        stdin, stdout, stderr = (
            self.cliente.exec_command(
                comando_sudo,
                get_pty=True
            )
        )


        stdin.write(
            self.password + "\n"
        )

        stdin.flush()


        salida = (
            stdout.read()
            .decode("utf-8", errors="replace")
            .strip()
        )

        error = (
            stderr.read()
            .decode("utf-8", errors="replace")
            .strip()
        )


        codigo_salida = (
            stdout.channel.recv_exit_status()
        )


        if codigo_salida != 0:

            raise Exception(
                "Error al ejecutar comando con sudo: "
                f"{error or salida}"
            )


        return {
            "salida": salida,
            "error": error,
            "codigo": codigo_salida
        }


    # ==================================================
    # PREPARAR PERMISOS
    # ==================================================

    def ejecutar_chown(self):

        if not self.cliente:

            raise Exception(
                "No hay conexión SSH establecida."
            )


        rutas = [
            (
                f"{self.RUTA_BASE_REMOTA}"
                "/AW100"
            ),
            (
                f"{self.RUTA_BASE_REMOTA}"
                "/AW200"
            )
        ]


        for ruta in rutas:

            self.ejecutar_sudo(
                f"chown -R kuka:kuka {ruta}"
            )


        return True


    # ==================================================
    # CONEXIÓN SFTP
    # ==================================================

    def conectar_sftp(self):

        if not self.cliente:

            raise Exception(
                "No hay conexión SSH establecida."
            )


        self.sftp = (
            self.cliente.open_sftp()
        )


        return self.sftp


    # ==================================================
    # LISTAR CARPETA REMOTA
    # ==================================================

    def listar_carpeta(self, ruta):

        if not self.sftp:

            raise Exception(
                "No hay conexión SFTP establecida."
            )


        archivos = (
            self.sftp.listdir_attr(ruta)
        )


        resultado = []


        for archivo in archivos:

            resultado.append({
                "nombre": archivo.filename,
                "tamano": archivo.st_size,
                "permisos": (
                    oct(archivo.st_mode)[-3:]
                )
            })


        return resultado


    # ==================================================
    # SUBIR UN ARCHIVO
    # ==================================================

    def subir_archivo(
        self,
        archivo_local,
        ruta_remota
    ):

        if not self.sftp:

            raise Exception(
                "No hay conexión SFTP establecida."
            )


        archivo_local = Path(
            archivo_local
        )


        if not archivo_local.exists():

            raise FileNotFoundError(
                "El archivo local no existe: "
                f"{archivo_local}"
            )


        if not archivo_local.is_file():

            raise ValueError(
                "La ruta local no corresponde "
                f"a un archivo: {archivo_local}"
            )


        self.sftp.put(
            str(archivo_local),
            ruta_remota
        )


        return True


    # ==================================================
    # VERIFICAR ARCHIVO REMOTO
    # ==================================================

    def verificar_archivo(
        self,
        archivo_local,
        ruta_remota
    ):

        if not self.sftp:

            raise Exception(
                "No hay conexión SFTP establecida."
            )


        archivo_local = Path(
            archivo_local
        )


        tamano_local = (
            archivo_local.stat().st_size
        )


        informacion_remota = (
            self.sftp.stat(ruta_remota)
        )


        tamano_remoto = (
            informacion_remota.st_size
        )


        if tamano_local != tamano_remoto:

            raise Exception(
                "El tamaño del archivo remoto "
                "no coincide con el archivo local. "
                f"Local: {tamano_local} bytes. "
                f"Remoto: {tamano_remoto} bytes."
            )


        return {
            "archivo_local": str(
                archivo_local
            ),
            "ruta_remota": ruta_remota,
            "tamano_local": tamano_local,
            "tamano_remoto": tamano_remoto,
            "verificado": True
        }


    # ==================================================
    # SUBIR LOS CUATRO ARCHIVOS DEL ROBOT
    # ==================================================

    def subir_archivos_robot(self):

        if not self.sftp:

            raise Exception(
                "No hay conexión SFTP establecida."
            )


        archivos = [
            {
                "local": Path(
                    "storage/AW100/0100.mp3"
                ),
                "remoto": (
                    f"{self.RUTA_BASE_REMOTA}"
                    "/AW100/0100.mp3"
                )
            },
            {
                "local": Path(
                    "storage/AW100/100.wav"
                ),
                "remoto": (
                    f"{self.RUTA_BASE_REMOTA}"
                    "/AW100/100.wav"
                )
            },
            {
                "local": Path(
                    "storage/AW200/0200.mp3"
                ),
                "remoto": (
                    f"{self.RUTA_BASE_REMOTA}"
                    "/AW200/0200.mp3"
                )
            },
            {
                "local": Path(
                    "storage/AW200/200.wav"
                ),
                "remoto": (
                    f"{self.RUTA_BASE_REMOTA}"
                    "/AW200/200.wav"
                )
            }
        ]


        # Validar todos los locales antes de
        # modificar un solo archivo del robot.

        for archivo in archivos:

            if not archivo["local"].exists():

                raise FileNotFoundError(
                    "No existe el archivo local: "
                    f"{archivo['local']}"
                )


        resultados = []


        for archivo in archivos:

            archivo_local = archivo["local"]
            ruta_remota = archivo["remoto"]


            print(
                "Subiendo "
                f"{archivo_local} "
                "a "
                f"{ruta_remota}"
            )


            self.subir_archivo(
                archivo_local,
                ruta_remota
            )


            verificacion = (
                self.verificar_archivo(
                    archivo_local,
                    ruta_remota
                )
            )


            resultados.append(
                verificacion
            )


            print(
                "Archivo verificado: "
                f"{ruta_remota}"
            )


        return resultados


    # ==================================================
    # CERRAR SFTP
    # ==================================================

    def cerrar_sftp(self):

        if self.sftp:

            self.sftp.close()

            self.sftp = None


    # ==================================================
    # CERRAR TODAS LAS CONEXIONES
    # ==================================================

    def cerrar(self):

        self.cerrar_sftp()


        if self.cliente:

            self.cliente.close()

            self.cliente = None