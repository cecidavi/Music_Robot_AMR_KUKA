from services.youtube_service import YoutubeService


youtube = YoutubeService()

info = youtube.obtener_info(
    "https://www.youtube.com/watch?v=Iy-dJwHVX84"
)

print(info)

youtube.descargar_audio(
    "https://www.youtube.com/watch?v=Iy-dJwHVX84"
)

print("Descarga completa")