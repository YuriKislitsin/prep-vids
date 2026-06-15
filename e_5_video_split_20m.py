#!/usr/bin/env python3
"""
Скрипт для разделения и конвертации MP4 видео для Telegram
"""

import subprocess
import sys
from pathlib import Path

# ============================================
# НАСТРОЙКИ
# ============================================
SOURCE_DIR = "/Volumes/D1/ !08.11.2025/HR"
SEGMENT_DURATION = 3600  # 60 минут в секундах

# Пути к ffmpeg (автоматически определяются)
FFMPEG_PATH = "/usr/local/Homebrew/bin/ffmpeg"
FFPROBE_PATH = "/usr/local/Homebrew/bin/ffprobe"

# ============================================


def get_video_duration(video_path):
    """Получение длительности видео в секундах"""
    try:
        result = subprocess.run([
            FFPROBE_PATH,
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(video_path)
        ], capture_output=True, text=True, check=True)
        
        duration = float(result.stdout.strip())
        return int(duration)
    except Exception as e:
        print(f"   ⚠️  Ошибка при получении длительности: {e}")
        return None


def convert_video(input_path, output_path, start_time=None, duration=None):
    """Конвертация видео в формат для Telegram"""
    cmd = [FFMPEG_PATH]
    
    if start_time is not None:
        cmd.extend(['-ss', str(start_time)])
    
    cmd.extend(['-i', str(input_path)])
    
    if duration is not None:
        cmd.extend(['-t', str(duration)])
    
    cmd.extend([
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-profile:v', 'high',
        '-level', '4.0',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-ar', '44100',
        '-movflags', '+faststart',
        '-y',
        str(output_path),
        '-loglevel', 'error',
        '-stats'
    ])
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Ошибка ffmpeg: {e}")
        return False


def process_video(video_path, output_dir):
    """Обработка одного видео файла"""
    filename = video_path.stem
    
    print(f"\n{'='*60}")
    print(f"📹 Обработка: {video_path.name}")
    print(f"   Путь: {video_path}")
    
    duration = get_video_duration(video_path)
    
    if duration is None:
        print("   ⚠️  Не удалось определить длительность, пропускаем...")
        return False
    
    print(f"   ⏱️  Длительность: {duration // 60} минут ({duration} сек)")
    
    if duration <= SEGMENT_DURATION:
        # Видео короче 60 минут - просто конвертируем
        print("   ⚙️  Конвертация (без разделения)...")
        output_path = output_dir / f"{filename}_telegram.mp4"
        
        if convert_video(video_path, output_path):
            print("   ✅ Готово!")
            return True
        else:
            print("   ❌ Ошибка при обработке")
            return False
    else:
        # Видео длиннее 60 минут - делим на части
        num_parts = (duration + SEGMENT_DURATION - 1) // SEGMENT_DURATION
        print(f"   ✂️  Разделение на {num_parts} частей...")
        
        success = True
        for i in range(num_parts):
            start_time = i * SEGMENT_DURATION
            part_num = i + 1
            
            print(f"   ⚙️  Часть {part_num}/{num_parts} (старт: {start_time // 60} мин)...")
            output_path = output_dir / f"{filename}_part{part_num}_telegram.mp4"
            
            if convert_video(video_path, output_path, start_time, SEGMENT_DURATION):
                print(f"   ✅ Часть {part_num} готова!")
            else:
                print(f"   ❌ Ошибка при обработке части {part_num}")
                success = False
        
        return success


def main():
    """Основная функция"""
    print("╔" + "="*60 + "╗")
    print("║" + " "*15 + "Обработка видео для Telegram" + " "*17 + "║")
    print("╚" + "="*60 + "╝")
    print()
    
    # Проверка исходной папки
    source_path = Path(SOURCE_DIR)
    if not source_path.exists():
        print(f"❌ Ошибка: Папка не найдена: {SOURCE_DIR}")
        sys.exit(1)
    
    # Создание папки для результатов
    output_dir = source_path / "processed_videos"
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Исходная папка: {SOURCE_DIR}")
    print(f"💾 Результаты:     {output_dir}")
    print(f"⏱️  Разделение:     По {SEGMENT_DURATION // 60} минут")
    print()
    print("🔍 Поиск MP4 файлов...")
    print("-" * 60)
    
    # Поиск всех MP4 файлов
    video_files = []
    for video_path in source_path.rglob("*.mp4"):
        if "processed_videos" not in str(video_path):
            video_files.append(video_path)
    
    total = len(video_files)
    print(f"Найдено файлов: {total}")
    
    if total == 0:
        print("❌ MP4 файлы не найдены")
        sys.exit(0)
    
    # Обработка файлов
    processed = 0
    successful = 0
    
    for idx, video_path in enumerate(video_files, 1):
        print(f"\n📊 Прогресс: {idx}/{total}")
        if process_video(video_path, output_dir):
            successful += 1
        processed += 1
    
    # Итоги
    print()
    print("=" * 60)
    print("╔" + "="*60 + "╗")
    print("║" + " "*18 + "ОБРАБОТКА ЗАВЕРШЕНА!" + " "*21 + "║")
    print("╚" + "="*60 + "╝")
    print()
    print("📊 Статистика:")
    print(f"   • Найдено файлов:     {total}")
    print(f"   • Обработано:         {processed}")
    print(f"   • Успешно:            {successful}")
    print(f"   • С ошибками:         {processed - successful}")
    print()
    print("📁 Результаты сохранены в:")
    print(f"   {output_dir}")
    print()
    print("✨ Все видео готовы для загрузки в Telegram!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Прервано пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)