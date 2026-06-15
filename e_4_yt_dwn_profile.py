import os
import re
from yt_dlp import YoutubeDL

# Функция для очистки имени файла от недопустимых символов
def sanitize_filename(filename):
    return re.sub(r'[^\w\s.-]', '', filename).strip()

# Параметры
channel_url = "https://www.youtube.com/@tyessenov"
output_path = "/Volumes/Без названия/Edu/Youtube"
max_videos = 50

# Настройки для yt-dlp
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Лучшее качество MP4
    'outtmpl': os.path.join(output_path, '%(channel)s/%(title)s.%(ext)s'),  # Шаблон имени файла
    'playlist_items': f'1-{max_videos}',  # Скачать первые 50 видео
    'quiet': False,
    'no_warnings': True,
    'extract_flat': False,
}

# Получение информации о канале
with YoutubeDL({'quiet': True}) as ydl:
    info = ydl.extract_info(channel_url, download=False)
    channel_name = sanitize_filename(info.get('channel', 'UnknownChannel'))

# Создание папки с названием канала
channel_folder = os.path.join(output_path, channel_name)
if not os.path.exists(channel_folder):
    os.makedirs(channel_folder)

# Обновление шаблона пути с учетом созданной папки
ydl_opts['outtmpl'] = os.path.join(channel_folder, '%(title)s.%(ext)s')

# Скачивание видео
try:
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([channel_url])
    print("Скачивание завершено!")
except Exception as e:
    print(f"Ошибка при скачивании: {str(e)}")