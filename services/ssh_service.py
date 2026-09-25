#services/ssh_service.py


import paramiko
from pathlib import Path


class SSHService:

    def __init__(self, host, usuario, password, puerto=22):

        self.host = host
        self.usuario = usuario
        self.password = password
        self.puerto = puerto

        self.cliente = None
        self.sftp = None


    def conectar(self):

        self.cliente = paramiko.SSHClient()

        self.cliente.load_system_host_keys()

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

    def ejecutar_sudo(self, comando):

        if not self.cliente:
            raise Exception("No hay conexión SSH establecida.")
        comado_sudo =f"sudo -S -p '' {comando}"
        stdin,stdout,srderr = self.cliente.exec_command(comado_sudo,get_pty=True)

        stdin.write(self.password + '\n')
        stdin.flush()

        salida = stdout.read().decode().strip()
        error = srderr.read().decode().strip()

        codigo_salida = stdout.channel.recv_exit_status()

        if codigo_salida !=0:
            raise Exception (f"Error al ejecutar Super Usuario: {error}")

        return {
            "salida": salida,
            "error": error,
            "codigo": codigo_salida
        }



    def ejecutar_chown(self):
        if not self.cliente:
            raise Exception("No hay conexión SSH establecida.")

        rutas = [
            "/home/kuka/userdata/kuka_audio/AW100",
            "/home/kuka/userdata/kuka_audio/AW200"
        ]

        for ruta in rutas:

            self.ejecutar_sudo(f"chown -R kuka:kuka {ruta}")

        return True



    def conectar_stfp(self):

        if not self.cliente:
            raise Exception("No hay conexión SSH establecida.")

        self.sftp = self.cliente.open_sftp()

        return self.sftp

#lo uso para probar la conexion a los robots
#despues para verificar si si existian los archivos dentro de las carpetas

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

    def subir_archivo(self, archivo_local, ruta_remota):

        if not self.sftp:
            raise Exception("No hay conexión SFTP establecida.")

        if not Path(archivo_local).exists():
            raise FileNotFoundError(f"El archivo local '{archivo_local}' no existe.")

        self.sftp.put(archivo_local, ruta_remota)
        
        return True

    def subir_archivos_robot(self):

        if not self.sftp:
            raise Exception("No hay conexión SFTP establecida.")

        archivos = [
            (Path("storage/AW100/0100.mp3"), "/home/kuka/userdata/kuka_audio/AW100/0100.mp3"),
            (Path("storage/AW200/0200.mp3"), "/home/kuka/userdata/kuka_audio/AW200/0200.mp3"),
            (Path("storage/AW100/100.wav"), "/home/kuka/userdata/kuka_audio/AW100/100.wav"),
            (Path("storage/AW200/200.wav"), "/home/kuka/userdata/kuka_audio/AW200/200.wav")      
                    
                    ]

        for archivo_local, ruta_remota in archivos:

            print(f"Subiendo {archivo_local} a {ruta_remota}")

            self.subir_archivo(str(archivo_local), ruta_remota)

        return True

    def cerrar_sftp(self):

        if self.sftp:
            self.sftp.close()
            self.sftp = None


    def cerrar(self):

        if self.cliente:
            self.cliente.close()
            self.cliente = None