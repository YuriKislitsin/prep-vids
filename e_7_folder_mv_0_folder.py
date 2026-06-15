import os
import shutil

# Путь к директории
source_directory = '/Volumes/Macintosh HD — данные/Users/mac/Downloads/!Edu/Дашкиев/'
destination_directory = source_directory  # Основная папка, куда будут перемещены файлы

# Проходим по всем подпапкам в директории
for root, dirs, files in os.walk(source_directory):
    for file_name in files:
        # Полный путь к файлу
        file_path = os.path.join(root, file_name)
        
        # Пропускаем файлы, которые уже находятся в основной папке
        if root == destination_directory:
            continue
        
        # Новый путь для перемещения файла
        new_file_path = os.path.join(destination_directory, file_name)
        
        # Проверяем, существует ли файл с таким же именем в основной папке
        if os.path.exists(new_file_path):
            print(f"Файл '{file_name}' уже существует в основной папке. Пропускаем его.")
            continue
        
        # Перемещаем файл в основную директорию
        shutil.move(file_path, new_file_path)
        print(f"Перемещен файл: '{file_path}' -> '{new_file_path}'")