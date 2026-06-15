import os

# Устанавливаем путь к корневой папке, где будет производиться поиск
root_dir = "/Volumes/Macintosh HD — данные/Users/mac/Downloads/!Edu/Janetakis/[Udemy] [Nick Janetakis] Docker для DevOps от разработки до продакшена (2025)/en"

# Проходим по всем файлам и подпапкам в корневой папке
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        file_path = os.path.join(foldername, filename)
        # Получаем название текущей папки
        folder_name = os.path.basename(foldername)
        # Создаем новое имя файла с добавлением названия папки
        new_filename = f"{folder_name} | {filename}"
        new_file_path = os.path.join(foldername, new_filename)
        # Переименовываем файл
        os.rename(file_path, new_file_path)
        print(f"Файл {file_path} был переименован в {new_file_path}")

print("Готово!")
