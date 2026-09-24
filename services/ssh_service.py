#services/ssh_service.py


import paramiko


class SSHService:

    def __init__(self, host, usuario, password, puerto=22):

        self.host = host
        self.usuario = usuario
        self.password = password
        self.puerto = puerto

        self.cliente = None


    def conectar(self):

        self.cliente = paramiko.SSHClient()

        self.cliente.load_system_host_keys()

        self.cliente.connect(
            hostname=self.host,
            port=self.puerto,
            username=self.usuario,
            password=self.password,
            timeout=10
        )

        return True


    def cerrar(self):

        if self.cliente:
            self.cliente.close()
            self.cliente = None

    def conectar_stfp(self):

        if not self.cliente:
            raise Exception("No hay conexión SSH establecida.")

        self.sftp = self.cliente.open_sftp()

        return self.sftp

    def listar_carpetas(self, ruta):

        if not self.sftp:
            raise Exception("No hay conexión SFTP establecida.")

        archivos = self.sftp.listdir_attr(ruta)

        resultado = []

        for archivo in archivos:

            resultado.append({
                "nombre": archivo.filename,
                "tamano": archivo.st_size,
                "permisos": oct(archivo.st_mode)[-3:]
            })

        return resultado

    def cerrar_sftp(self):

        if self.sftp:
            self.sftp.close()
            self.sftp = None

        if self.cliente:
            self.cliente.close()
            self.cliente = None