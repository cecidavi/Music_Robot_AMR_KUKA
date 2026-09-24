import paramiko


class SFTPService:

    BASE_AUDIO_PATH = "/home/kuka/userdata/kuka_audio"

    def __init__(self, ip, usuario, password, puerto=22):
        self.ip = ip
        self.usuario = usuario
        self.password = password
        self.puerto = puerto

    def conectar(self):

        ssh = paramiko.SSHClient()

        # SOLO PARA LA PRUEBA INICIAL.
        # Después configuraremos known_hosts correctamente.
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        ssh.connect(
            hostname=self.ip,
            port=self.puerto,
            username=self.usuario,
            password=self.password,
            timeout=10
        )

        sftp = ssh.open_sftp()

        return ssh, sftp

    def listar_carpeta(self, carpeta):

        ssh = None
        sftp = None

        try:

            ssh, sftp = self.conectar()

            ruta = f"{self.BASE_AUDIO_PATH}/{carpeta}"

            archivos = sftp.listdir_attr(ruta)

            resultado = []

            for archivo in archivos:

                resultado.append({
                    "nombre": archivo.filename,
                    "tamano": archivo.st_size,
                    "permisos": oct(archivo.st_mode)[-3:]
                })

            return resultado

        finally:

            if sftp:
                sftp.close()

            if ssh:
                ssh.close()