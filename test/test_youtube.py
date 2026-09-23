
#test/test_youtube.py



from services.youtube_service import YoutubeService

#esta para obtener los datos del video y saber si esta funcionando
youtube = YoutubeService()

info = youtube.obtener_info(
    "https://www.youtube.com/watch?v=Iy-dJwHVX84"
)

print(info)

#este metodo funciona bien puedo tener los parametros que esperaba 

youtube.descargar_audio(
    "https://www.youtube.com/watch?v=Iy-dJwHVX84"
)

print("Descarga completa")

#el video de Youtube ya se pasa a mp3 y hay otro test que lo convierte en mp3 y wav


