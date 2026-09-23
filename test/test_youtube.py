
#test/test_youtube.py



from services.youtube_service import YoutubeService

#esta para obtener los datos del video y saber si esta funcionando
youtube = YoutubeService()

info = youtube.obtener_info(
    "https://www.youtube.com/watch?v=Iy-dJwHVX84"
)

print(info)

#este metodo funciona bien puedo tener los parametros que esperaba 


#esto es para descargar el video
youtube.descargar_audio(
    "https://www.youtube.com/watch?v=Iy-dJwHVX84",
    "original.%(ext)s"  # esta parte es para renombrar el archivo por original
                        # para mi es mas sencillo esto pero si no se ocupa retirarlo y en youtube_service.py
)

print("Descarga completa")

#notas el audio se descarga en formato webn 
#osea si funciona pero aun no agrego el ffmpeg para convertirlo a mp3
#pero en si esta funcionado

