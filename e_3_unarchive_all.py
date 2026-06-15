import os
import zipfile
import rarfile
import tarfile
import py7zr
import subprocess
from pathlib import Path
from send2trash import send2trash  # Импортируем модуль для отправки в корзину

# Путь к папке Downloads
DOWNLOADS_PATH = "/Volumes/Без названия/"

# Поддерживаемые расширения архивов
ARCHIVE_EXTENSIONS = ('.zip', '.rar', '.tar', '.tar.gz', '.tgz', '.7z')

def extract_zip(file_path, extract_to):
    """Разархивировать ZIP-файл."""
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Успешно разархивирован: {file_path}")
        send2trash(file_path)  # Отправляем архив в корзину
        print(f"Архив отправлен в корзину: {file_path}")
    except Exception as e:
        print(f"Ошибка при разархивировании {file_path}: {e}")

def extract_rar(file_path, extract_to):
    """Разархивировать RAR-файл."""
    try:
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(extract_to)
        print(f"Успешно разархивирован: {file_path}")
        send2trash(file_path)  # Отправляем архив в корзину
        print(f"Архив отправлен в корзину: {file_path}")
    except Exception as e:
        print(f"Ошибка при разархивировании {file_path}: {e}")

def extract_tar(file_path, extract_to):
    """Разархивировать TAR, TAR.GZ или TGZ файл."""
    try:
        with tarfile.open(file_path, 'r:*') as tar_ref:
            tar_ref.extractall(extract_to)
        print(f"Успешно разархивирован: {file_path}")
        send2trash(file_path)  # Отправляем архив в корзину
        print(f"Архив отправлен в корзину: {file_path}")
    except Exception as e:
        print(f"Ошибка при разархивировании {file_path}: {e}")

def extract_7z(file_path, extract_to):
    """Разархивировать 7Z-файл."""
    try:
        with py7zr.SevenZipFile(file_path, mode='r') as z:
            z.extractall(extract_to)
        print(f"Успешно разархивирован: {file_path}")
        send2trash(file_path)  # Отправляем архив в корзину
        print(f"Архив отправлен в корзину: {file_path}")
    except Exception as e:
        print(f"Ошибка при разархивировании {file_path}: {e}")

def extract_archive(file_path):
    """Определить тип архива и разархивировать его."""
    file_path = Path(file_path)
    extract_to = file_path.parent  # Извлечь в ту же папку, где находится архив

    if file_path.suffix.lower() == '.zip':
        extract_zip(file_path, extract_to)
    elif file_path.suffix.lower() == '.rar':
        extract_rar(file_path, extract_to)
    elif file_path.suffix.lower() in ('.tar', '.gz', '.tgz'):
        extract_tar(file_path, extract_to)
    elif file_path.suffix.lower() == '.7z':
        extract_7z(file_path, extract_to)
    else:
        print(f"Неподдерживаемый формат: {file_path}")

def main():
    # Проверяем, существует ли папка Downloads
    if not os.path.exists(DOWNLOADS_PATH):
        print(f"Папка {DOWNLOADS_PATH} не найдена!")
        return

    # Рекурсивно обходим все файлы в папке Downloads
    for root, _, files in os.walk(DOWNLOADS_PATH):
        for file in files:
            if file.lower().endswith(ARCHIVE_EXTENSIONS):
                file_path = os.path.join(root, file)
                print(f"Обнаружен архив: {file_path}")
                extract_archive(file_path)

    print("Разархивирование завершено.")

if __name__ == "__main__":
    main()