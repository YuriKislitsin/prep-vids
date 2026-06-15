#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор обложек для видео файлов
Создает коллаж 1200x1200 из 18 скриншотов видео (6 строк x 3 колонки), 400x200, подогнанные по ширине
"""

# =============================================
# НАСТРОЙКИ - ИЗМЕНИТЕ ПУТЬ К ПАПКЕ ЗДЕСЬ
# =============================================
VIDEO_FOLDER = "/Users/yk/Downloads/Projects/Janetakis/[Udemy] [Nick Janetakis] Docker для DevOps от разработки до продакшена (2025)/ru/"
# =============================================

import os
import cv2
from PIL import Image, ImageDraw, ImageFont
import textwrap
from pathlib import Path
import numpy as np

def get_video_duration(video_path):
    """
    Получает длительность видео в секундах
    """
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        cap.release()
        
        if fps > 0:
            duration = frame_count / fps
            return duration
        else:
            return None
    except Exception as e:
        print(f"❌ Ошибка при получении длительности видео: {e}")
        return None

def extract_frame_at_time(video_path, time_seconds):
    """
    Извлекает кадр из видео в указанное время
    """
    try:
        cap = cv2.VideoCapture(video_path)
        
        # Устанавливаем позицию в миллисекундах
        cap.set(cv2.CAP_PROP_POS_MSEC, time_seconds * 1000)
        
        # Читаем кадр
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            # Конвертируем BGR в RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return Image.fromarray(frame_rgb)
        else:
            return None
            
    except Exception as e:
        print(f"❌ Ошибка при извлечении кадра: {e}")
        return None

def resize_and_crop_frame(frame, target_width=400, target_height=200):
    """
    Изменяет размер и обрезает кадр до заданного размера 400x200, подгоняя по ширине
    """
    # Получаем размеры исходного кадра
    width, height = frame.size
    
    # Вычисляем соотношение сторон
    aspect_ratio = width / height
    
    # Масштабируем по ширине (target_width), сохраняя пропорции
    new_width = target_width
    new_height = int(target_width / aspect_ratio)
    
    # Масштабируем кадр
    resized_frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Обрезаем до размера target_width x target_height, центрируя по вертикали
    if new_height >= target_height:
        # Если высота больше или равна целевой, обрезаем по центру
        top = (new_height - target_height) // 2
        bottom = top + target_height
    else:
        # Если высота меньше целевой, масштабируем заново, чтобы подогнать по высоте
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
        resized_frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Обрезаем по ширине, центрируя
        left = (new_width - target_width) // 2
        right = left + target_width
        top = 0
        bottom = target_height
        resized_frame = resized_frame.crop((left, top, right, bottom))
        return resized_frame
    
    # Обрезаем до целевого размера
    cropped_frame = resized_frame.crop((0, top, target_width, bottom))
    
    return cropped_frame

def create_fallback_thumbnail(video_name, size=1200):
    """
    Создает запасную миниатюру с названием видео, если не удалось извлечь кадры
    """
    img = Image.new('RGB', (size, size), color='black')
    draw = ImageDraw.Draw(img)
    
    # Пути к возможным шрифтам
    font_paths = [
        '/System/Library/Fonts/Arial Narrow.ttf',
        '/System/Library/Fonts/ArialNarrow.ttf',
        '/Library/Fonts/Arial Narrow.ttf',
        '/System/Library/Fonts/Arial.ttf',
        '/System/Library/Fonts/Helvetica.ttc'
    ]
    
    font_path = None
    for path in font_paths:
        if os.path.exists(path):
            font_path = path
            break
    
    text = video_name.upper()
    
    try:
        # Простой алгоритм подбора размера шрифта для 1200x1200
        font_size = 45  # Увеличенный размер для большего коллажа
        max_width = size - 60
        
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
        
        # Разбиваем текст на строки
        lines = textwrap.wrap(text, width=20)
        
        # Вычисляем позицию для центрирования
        total_height = len(lines) * font_size + (len(lines) - 1) * 8
        start_y = (size - total_height) // 2
        
        # Рисуем текст
        current_y = start_y
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (size - text_width) // 2
            draw.text((x, current_y), line, fill='white', font=font)
            current_y += font_size + 8
            
    except Exception as e:
        print(f"⚠️ Ошибка при создании запасной миниатюры: {e}")
        # Просто рисуем прямоугольник с текстом "ERROR"
        draw.rectangle([size//4, size//2-30, 3*size//4, size//2+30], fill='red')
        draw.text((size//2-30, size//2-15), "ERROR", fill='white')
    
    return img

def get_optimal_font_size_for_title(text, font_path, max_width, max_height, max_font_size=160):
    """
    Определяет оптимальный размер шрифта для заголовка поверх всего коллажа (увеличено для 1200x1200)
    """
    font_size = max_font_size
    
    while font_size > 25:  # Минимальный размер шрифта для заголовка
        try:
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.load_default()
            
            # Создаем временное изображение для измерения текста
            temp_img = Image.new('RGB', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            
            # Разбиваем текст на строки
            max_chars_per_line = max(12, min(40, int(max_width / (font_size * 0.6))))
            lines = textwrap.wrap(text, width=max_chars_per_line)
            
            # Если получилось слишком много строк, попробуем увеличить длину строки
            if len(lines) > 6:
                max_chars_per_line = min(55, int(max_width / (font_size * 0.5)))
                lines = textwrap.wrap(text, width=max_chars_per_line)
            
            total_height = 0
            max_line_width = 0
            line_height = 0
            
            for line in lines:
                bbox = temp_draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                line_height = max(line_height, bbox[3] - bbox[1])
                max_line_width = max(max_line_width, line_width)
            
            # Общая высота с учетом отступов между строками
            total_height = len(lines) * line_height + (len(lines) - 1) * (line_height * 0.2)
            
            # Проверяем, помещается ли текст
            if max_line_width <= max_width and total_height <= max_height:
                return font_size, lines, line_height
                
        except Exception as e:
            print(f"Ошибка при определении размера шрифта заголовка: {e}")
        
        font_size -= 8  # Уменьшаем с большим шагом для больших размеров
    
    # Если не удалось подобрать размер, возвращаем минимальные значения
    lines = textwrap.wrap(text, width=35)
    return font_size, lines, 30

def add_title_overlay(collage, text, font_path):
    """
    Добавляет заголовок поверх всего коллажа с полупрозрачной подложкой
    """
    # Создаем копию коллажа
    collage_with_title = collage.copy()
    
    # Размеры коллажа
    width, height = collage.size
    
    # Параметры для текстовой области (по центру коллажа) - увеличено для 1200x1200
    text_area_height = min(300, height // 3)  # Максимум 300px или треть высоты
    text_area_y = (height - text_area_height) // 2  # Центрируем по вертикали
    
    # Создаем полупрозрачный черный прямоугольник для текста
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Делаем подложку с отступами от краев
    padding = 60  # Увеличенный отступ для большего коллажа
    overlay_draw.rectangle([
        padding, 
        text_area_y - padding//2, 
        width - padding, 
        text_area_y + text_area_height + padding//2
    ], fill=(0, 0, 0, 200))
    
    # Накладываем подложку на коллаж
    collage_with_title = Image.alpha_composite(collage_with_title.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(collage_with_title)
    
    # Определяем оптимальный размер шрифта
    max_text_width = width - 150  # Отступы по 75px с каждой стороны
    max_text_height = text_area_height - 60  # Отступы сверху и снизу
    
    font_size, lines, line_height = get_optimal_font_size_for_title(
        text, font_path, max_text_width, max_text_height
    )
    
    try:
        # Пытаемся загрузить шрифт как жирный
        if font_path:
            try:
                # Сначала пытаемся найти жирную версию Arial Narrow
                bold_font_paths = [
                    font_path.replace('.ttf', ' Bold.ttf'),
                    font_path.replace('.ttf', 'Bold.ttf'),
                    font_path.replace('Arial Narrow', 'Arial Narrow Bold'),
                    font_path.replace('Arial', 'Arial Bold'),
                ]
                
                font = None
                for bold_path in bold_font_paths:
                    if os.path.exists(bold_path):
                        font = ImageFont.truetype(bold_path, font_size)
                        break
                
                # Если жирный шрифт не найден, используем обычный
                if font is None:
                    font = ImageFont.truetype(font_path, font_size)
                    
            except Exception:
                font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
        
        # Вычисляем общую высоту текстового блока
        total_text_height = len(lines) * line_height + (len(lines) - 1) * (line_height * 0.2)
        
        # Начальная позиция Y для центрирования в текстовой области
        start_y = text_area_y + (text_area_height - total_text_height) // 2
        
        # Рисуем каждую строку
        current_y = start_y
        for line in lines:
            # Получаем размеры строки для центрирования по горизонтали
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            
            # Центрируем по горизонтали
            x = (width - text_width) // 2
            
            # Рисуем контур для создания эффекта жирности (если не удалось загрузить жирный шрифт)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, current_y + dy), line, fill='black', font=font)
            
            # Рисуем основной текст белым цветом
            draw.text((x, current_y), line, fill='white', font=font)
            
            # Переходим к следующей строке
            current_y += line_height + int(line_height * 0.2)
            
    except Exception as e:
        print(f"⚠️ Ошибка при добавлении заголовка: {e}")
        # Рисуем простой текст в случае ошибки
        simple_text = text[:30] + "..." if len(text) > 30 else text
        draw.text((width//2 - 150, height//2), simple_text, fill='white')
    
    return collage_with_title

def create_thumbnail(video_path, output_path):
    """
    Создает миниатюру-коллаж из 18 скриншотов видео с названием (6 строк x 3 колонки)
    """
    video_name = Path(video_path).stem
    print(f"🎬 Обрабатывается: {video_name}")
    
    # Получаем длительность видео
    duration = get_video_duration(video_path)
    
    if duration is None or duration < 1:
        print(f"❌ Не удалось получить длительность видео или видео слишком короткое")
        # Создаем запасную обложку
        fallback = create_fallback_thumbnail(video_name, 1200)
        fallback.save(output_path, 'JPEG', quality=95)
        print(f"⚠️ Создана запасная обложка: {output_path}")
        return
    
    # Вычисляем временные метки для скриншотов (18 кадров равномерно распределенных)
    # Начинаем с 5% и заканчиваем на 95%, чтобы избежать черных кадров в начале/конце
    timestamps = [duration * (i / 100.0) for i in range(5, 96, 5)]  # 5%, 10%, 15%, ..., 95% = 19 точек
    timestamps = timestamps[:18]  # Берем первые 18 точек
    
    print(f"⏱️ Длительность видео: {duration:.1f} сек")
    print(f"📸 Извлекаются 18 кадров на: {[f'{t:.1f}с' for t in timestamps]}")
    
    # Параметры сетки 6 строк x 3 колонки
    rows = 6
    cols = 3
    border_width = 0   # Без обводки для точного соответствия 1200x1200
    frame_width = 400  # Ширина каждого кадра (1200 / 3 = 400)
    frame_height = 200 # Высота каждого кадра (1200 / 6 = 200)

    print(f"🔧 Размер кадра: {frame_width}x{frame_height}")
    print(f"🔧 Сетка: {rows} строк x {cols} колонки = {rows*cols} кадров")
    
    # Извлекаем кадры
    frames = []
    for i, timestamp in enumerate(timestamps):
        frame = extract_frame_at_time(video_path, timestamp)
        if frame is not None:
            # Изменяем размер и обрезаем кадр до 400x200, подгоняя по ширине
            final_frame = resize_and_crop_frame(frame, target_width=frame_width, target_height=frame_height)
            frames.append(final_frame)
            print(f"✅ Кадр {i+1}/18 извлечен ({timestamp:.1f}с)")
        else:
            print(f"❌ Не удалось извлечь кадр {i+1}/18 ({timestamp:.1f}с)")
            # Создаем черный прямоугольник с размерами кадра
            black_frame = Image.new('RGB', (frame_width, frame_height), color='black')
            frames.append(black_frame)
    
    # Если не удалось извлечь ни одного кадра, создаем запасную обложку
    if all(np.array(frame).sum() == 0 for frame in frames):  # Все кадры черные
        print(f"❌ Не удалось извлечь кадры, создаем запасную обложку")
        fallback = create_fallback_thumbnail(video_name, 1200)
        fallback.save(output_path, 'JPEG', quality=95)
        print(f"⚠️ Создана запасная обложка: {output_path}")
        return
    
    # Получаем путь к шрифту Arial Narrow
    font_paths = [
        '/System/Library/Fonts/Arial Narrow.ttf',
        '/System/Library/Fonts/ArialNarrow.ttf',
        '/Library/Fonts/Arial Narrow.ttf',
        '/System/Library/Fonts/Arial.ttf',
        '/System/Library/Fonts/Helvetica.ttc'
    ]
    
    font_path = None
    for path in font_paths:
        if os.path.exists(path):
            font_path = path
            break
    
    # Создаем коллаж 1200x1200 из 18 кадров (6 строк x 3 колонки)
    try:
        collage = Image.new('RGB', (1200, 1200), color='black')
        
        # Размещаем кадры в сетке 6x3
        for i in range(min(18, len(frames))):
            row = i // cols
            col = i % cols
            
            # Вычисляем координаты
            x = col * frame_width
            y = row * frame_height
            
            collage.paste(frames[i], (x, y))
            
        # Добавляем заголовок поверх всего коллажа
        text = video_name.upper()
        collage_with_title = add_title_overlay(collage, text, font_path)
        
        # Сохраняем коллаж с заголовком
        collage_with_title.save(output_path, 'JPEG', quality=95)
        print(f"✅ Создана обложка-коллаж 6x3 ({frame_width}x{frame_height} каждый кадр): {output_path}")
        
    except Exception as e:
        print(f"❌ Ошибка при создании коллажа для '{video_name}': {e}")
        # В случае ошибки создаем запасную обложку
        fallback = create_fallback_thumbnail(video_name, 1200)
        fallback.save(output_path, 'JPEG', quality=95)
        print(f"⚠️ Создана запасная обложка: {output_path}")

def find_mp4_files_recursive(root_folder):
    """
    Рекурсивно ищет все .mp4 файлы в папке и всех подпапках
    """
    mp4_files = []
    
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.mp4'):
                mp4_files.append(os.path.join(root, file))
    
    return mp4_files

def main():
    """
    Основная функция
    """
    print("=" * 60)
    print("🎬 ГЕНЕРАТОР ОБЛОЖЕК ДЛЯ ВИДЕО ФАЙЛОВ")
    print("📐 Размер: 1200x1200 (6 строк x 3 колонки = 18 кадров)")
    print("=" * 60)
    
    # Используем путь из переменной в начале файла
    video_folder = VIDEO_FOLDER
    print(f"📂 Папка для обработки: {video_folder}")
    
    # Проверяем существование папки
    if not os.path.exists(video_folder):
        print(f"❌ Папка не найдена: {video_folder}")
        print("💡 Измените переменную VIDEO_FOLDER в начале скрипта")
        print("Проверьте путь и убедитесь, что диск подключен")
        input("📋 Нажмите Enter для выхода...")
        return
    
    # Проверяем наличие OpenCV
    try:
        import cv2
        print(f"✅ OpenCV версия: {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV не установлен. Установите его командой: pip install opencv-python")
        input("📋 Нажмите Enter для выхода...")
        return
    
    # Рекурсивно ищем все .mp4 файлы в папке и подпапках
    print(f"🔍 Поиск .mp4 файлов в папке и всех подпапках...")
    mp4_files = find_mp4_files_recursive(video_folder)
    
    if not mp4_files:
        print(f"❌ В папке и подпапках не найдено файлов .mp4")
        print(f"📂 Проверяемая папка: {video_folder}")
        input("📋 Нажмите Enter для выхода...")
        return
    
    print(f"📁 Найдено {len(mp4_files)} видео файлов")
    print("ℹ️ Создается коллаж 6 строк x 3 колонки = 18 кадров из каждого видео")
    print("-" * 60)
    
    # Группируем файлы по папкам для удобства вывода
    folders_processed = set()
    processed_count = 0
    errors_count = 0
    
    # Обрабатываем каждый видео файл
    for i, mp4_file in enumerate(mp4_files, 1):
        # Получаем папку файла
        file_folder = os.path.dirname(mp4_file)
        
        # Выводим информацию о новой обрабатываемой папке
        if file_folder not in folders_processed:
            relative_path = os.path.relpath(file_folder, video_folder)
            if relative_path == ".":
                print(f"📂 Обрабатывается корневая папка:")
            else:
                print(f"📂 Обрабатывается подпапка: {relative_path}")
            folders_processed.add(file_folder)
        
        # Формируем путь для выходного .jpg файла (в той же папке что и .mp4)
        file_name = Path(mp4_file).stem  # Имя без расширения
        jpg_file = os.path.join(file_folder, f"{file_name}.jpg")
        
        print(f"[{i}/{len(mp4_files)}] ", end="")
        
        # Проверяем, существует ли уже обложка
        if os.path.exists(jpg_file):
            print(f"⏭️ Обложка уже существует: {file_name}.jpg")
            processed_count += 1
            continue
        
        # Создаем обложку
        try:
            create_thumbnail(mp4_file, jpg_file)
            processed_count += 1
        except Exception as e:
            print(f"❌ Критическая ошибка при обработке '{file_name}': {e}")
            errors_count += 1
        
        print("-" * 40)
    
    print("-" * 60)
    print(f"🎉 Обработка завершена!")
    print(f"📊 Обработано папок: {len(folders_processed)}")
    print(f"🖼️ Успешно создано обложек: {processed_count}")
    if errors_count > 0:
        print(f"❌ Ошибок при обработке: {errors_count}")
    print("💡 Для использования скрипта необходимо установить: pip install opencv-python pillow")
    print("-" * 60)
    
    # Ждем нажатия клавиши перед выходом
    input("📋 Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()