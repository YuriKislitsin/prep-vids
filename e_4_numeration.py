#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой скрипт для нумерации файлов в папке Semaev Devops
"""

import os
from pathlib import Path

# Путь к вашей папке
FOLDER_PATH = "/Volumes/Без названия/YT-DL/Brit Docker"

def number_files_in_folders():
    """Добавляет нумерацию к файлам в каждой подпапке"""
    
    root_path = Path(FOLDER_PATH)
    
    # Проверяем существование папки
    if not root_path.exists():
        print(f"❌ Папка не найдена: {FOLDER_PATH}")
        print("Убедитесь, что внешний диск подключён")
        return
    
    print(f"🎯 Обрабатываю папку: {FOLDER_PATH}")
    print("-" * 60)
    
    # Обходим все папки и подпапки
    for current_dir, subdirs, files in os.walk(root_path):
        current_path = Path(current_dir)
        
        # Фильтруем только видео и аудио файлы (обычно из YT-DL)
        video_extensions = {'.mp4', '.mkv', '.webm', '.m4a', '.mp3', '.opus'}
        files_to_number = []
        
        for filename in files:
            file_path = Path(filename)
            if file_path.suffix.lower() in video_extensions and not filename.startswith('.'):
                files_to_number.append(filename)
        
        if not files_to_number:
            continue
        
        # Показываем какую папку обрабатываем
        relative_path = current_path.relative_to(root_path) if current_path != root_path else "(корневая папка)"
        print(f"📁 {relative_path}")
        print(f"   Найдено файлов: {len(files_to_number)}")
        
        # Сортируем файлы по имени
        files_to_number.sort()
        
        # Нумеруем файлы
        counter = 1
        for filename in files_to_number:
            old_path = current_path / filename
            
            # Проверяем, не пронумерован ли уже
            if filename[:3].isdigit() and filename[3] == '_':
                print(f"   ⏭️  Уже пронумерован: {filename}")
                continue
            
            # Создаём новое имя
            file_extension = Path(filename).suffix
            name_without_ext = Path(filename).stem
            new_filename = f"{counter:03d}_{name_without_ext}{file_extension}"
            new_path = current_path / new_filename
            
            # Переименовываем файл
            try:
                old_path.rename(new_path)
                print(f"   ✅ {filename[:50]}{'...' if len(filename) > 50 else ''}")
                print(f"      → {new_filename}")
                counter += 1
            except OSError as e:
                print(f"   ❌ Ошибка: {filename} - {e}")
        
        print(f"   📊 Обработано: {counter - 1} файлов\n")

if __name__ == "__main__":
    print("🎬 Нумерация файлов YouTube-DL для Semaev Devops")
    print("=" * 50)
    
    try:
        number_files_in_folders()
        print("✅ Всё готово!")
    except KeyboardInterrupt:
        print("\n❌ Прервано пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой скрипт для нумерации файлов в папке Semaev Devops
"""

import os
from pathlib import Path

# Путь к вашей папке
FOLDER_PATH = "/Volumes/Без названия/YT-DL/Semaev Devops"

def number_files_in_folders():
    """Добавляет нумерацию к файлам в каждой подпапке"""
    
    root_path = Path(FOLDER_PATH)
    
    # Проверяем существование папки
    if not root_path.exists():
        print(f"❌ Папка не найдена: {FOLDER_PATH}")
        print("Убедитесь, что внешний диск подключён")
        return
    
    print(f"🎯 Обрабатываю папку: {FOLDER_PATH}")
    print("-" * 60)
    
    # Обходим все папки и подпапки
    for current_dir, subdirs, files in os.walk(root_path):
        current_path = Path(current_dir)
        
        # Фильтруем только видео и аудио файлы (обычно из YT-DL)
        video_extensions = {'.mp4', '.mkv', '.webm', '.m4a', '.mp3', '.opus'}
        files_to_number = []
        
        for filename in files:
            file_path = Path(filename)
            if file_path.suffix.lower() in video_extensions and not filename.startswith('.'):
                files_to_number.append(filename)
        
        if not files_to_number:
            continue
        
        # Показываем какую папку обрабатываем
        relative_path = current_path.relative_to(root_path) if current_path != root_path else "(корневая папка)"
        print(f"📁 {relative_path}")
        print(f"   Найдено файлов: {len(files_to_number)}")
        
        # Сортируем файлы по имени
        files_to_number.sort()
        
        # Нумеруем файлы
        counter = 1
        for filename in files_to_number:
            old_path = current_path / filename
            
            # Проверяем, не пронумерован ли уже
            if filename[:3].isdigit() and filename[3] == '_':
                print(f"   ⏭️  Уже пронумерован: {filename}")
                continue
            
            # Создаём новое имя
            file_extension = Path(filename).suffix
            name_without_ext = Path(filename).stem
            new_filename = f"{counter:03d}_{name_without_ext}{file_extension}"
            new_path = current_path / new_filename
            
            # Переименовываем файл
            try:
                old_path.rename(new_path)
                print(f"   ✅ {filename[:50]}{'...' if len(filename) > 50 else ''}")
                print(f"      → {new_filename}")
                counter += 1
            except OSError as e:
                print(f"   ❌ Ошибка: {filename} - {e}")
        
        print(f"   📊 Обработано: {counter - 1} файлов\n")

if __name__ == "__main__":
    print("🎬 Нумерация файлов YouTube-DL для Semaev Devops")
    print("=" * 50)
    
    try:
        number_files_in_folders()
        print("✅ Всё готово!")
    except KeyboardInterrupt:
        print("\n❌ Прервано пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")