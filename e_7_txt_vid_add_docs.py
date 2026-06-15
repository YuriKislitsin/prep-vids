import os

# Укажите путь к вашей директории
directory = '/Users/yk/Downloads/Projects/Janetakis/[Udemy] [Nick Janetakis] Docker для DevOps от разработки до продакшена (2025)/ru/'

# Определите расширения видеофайлов
video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv')

# Обход всех файлов и папок в указанной директории
for root, dirs, files in os.walk(directory):
    for file in files:
        # Проверяем, является ли файл видеофайлом
        if file.lower().endswith(video_extensions):
            # Создаем имя текстового файла
            text_file_name = os.path.splitext(file)[0] + '.txt'
            text_file_path = os.path.join(root, text_file_name)
            
            # Записываем имя видеофайла в текстовый документ
            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(file)

print("Текстовые файлы успешно созданы.")