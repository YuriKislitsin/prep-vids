import os
import sys
from pathlib import Path

def split_video(input_file, target_size_mb=200):
    """
    Разбивает видео на части заданного размера
    
    Args:
        input_file: путь к исходному видео файлу
        target_size_mb: целевой размер каждой части в мегабайтах
    """
    try:
        from moviepy import VideoFileClip
    except ImportError:
        print("❌ Ошибка: библиотека moviepy не установлена")
        print("Установите её командой: pip install moviepy")
        return
    
    # Проверка существования файла
    if not os.path.exists(input_file):
        print(f"❌ Ошибка: файл {input_file} не найден")
        return
    
    input_path = Path(input_file)
    output_dir = input_path.parent
    base_name = input_path.stem
    
    print(f"📂 Исходный файл: {input_file}")
    print(f"📁 Папка для сохранения: {output_dir}")
    print(f"📏 Целевой размер части: {target_size_mb} МБ")
    print("-" * 60)
    
    # Анализ видео
    print("🔍 Анализ видео...")
    try:
        temp_video = VideoFileClip(input_file)
        total_duration = temp_video.duration
        file_size = os.path.getsize(input_file) / (1024 * 1024)  # в МБ
        
        print(f"⏱️  Длительность: {total_duration:.2f} сек ({total_duration/60:.2f} мин)")
        print(f"💾 Размер файла: {file_size:.2f} МБ")
        print(f"🎬 Разрешение: {temp_video.size[0]}x{temp_video.size[1]}")
        print(f"🎞️  FPS: {temp_video.fps}")
        
        # Расчет примерного битрейта
        avg_bitrate = (file_size * 8) / total_duration  # Мбит/с
        print(f"📊 Средний битрейт: {avg_bitrate:.2f} Мбит/с")
        
        temp_video.close()
        
        print("-" * 60)
        
        # Начальная оценка длительности части
        chunk_duration = (target_size_mb * 8) / avg_bitrate
        print(f"⏰ Начальная оценка длительности части: ~{chunk_duration:.2f} сек")
        print(f"✂️  Примерное количество частей: {int(total_duration / chunk_duration) + 1}")
        print("-" * 60)
        
        # Разбивка видео с адаптивной корректировкой
        part_num = 1
        current_start = 0.0
        tolerance_mb = 10  # Допустимое отклонение в МБ
        
        while current_start < total_duration:
            # Оценка конечного времени для этой части
            estimated_end = min(current_start + chunk_duration, total_duration)
            
            print(f"\n🎬 Обработка части {part_num}")
            print(f"   ⏱️  Начальная оценка: {current_start:.2f}s - {estimated_end:.2f}s")
            
            # Создаем тестовый клип для проверки размера
            test_video = VideoFileClip(input_file)
            
            # Итеративный поиск правильной длительности
            best_end = estimated_end
            attempt = 0
            max_attempts = 5
            
            while attempt < max_attempts:
                try:
                    test_clip = test_video.subclipped(current_start, best_end)
                    
                    # Создаем временный файл для проверки размера
                    temp_output = output_dir / f"temp_test_{part_num}.mp4"
                    
                    test_clip.write_videofile(
                        str(temp_output),
                        codec='libx264',
                        audio_codec='aac',
                        temp_audiofile='temp-audio.m4a',
                        remove_temp=True,
                        preset='medium',
                        ffmpeg_params=['-movflags', '+faststart'],
                        logger=None
                    )
                    
                    test_clip.close()
                    
                    # Проверяем размер
                    actual_size = os.path.getsize(temp_output) / (1024 * 1024)
                    print(f"   🔍 Попытка {attempt + 1}: {best_end - current_start:.2f}s → {actual_size:.2f} МБ")
                    
                    # Если размер в пределах допустимого
                    if abs(actual_size - target_size_mb) <= tolerance_mb or best_end >= total_duration:
                        # Переименовываем временный файл в финальный
                        final_output = output_dir / f"{base_name}_part{part_num:03d}.mp4"
                        temp_output.rename(final_output)
                        print(f"   ✅ Создано: {actual_size:.2f} МБ")
                        current_start = best_end
                        break
                    
                    # Корректируем длительность на основе фактического размера
                    size_ratio = target_size_mb / actual_size
                    duration_adjustment = (best_end - current_start) * (size_ratio - 1)
                    
                    # Ограничиваем корректировку
                    duration_adjustment = max(min(duration_adjustment, 60), -60)
                    best_end = min(best_end + duration_adjustment, total_duration)
                    
                    # Удаляем временный файл
                    if temp_output.exists():
                        temp_output.unlink()
                    
                    attempt += 1
                    
                except Exception as e:
                    print(f"   ❌ Ошибка при попытке {attempt + 1}: {e}")
                    # Удаляем временный файл если есть
                    if temp_output.exists():
                        temp_output.unlink()
                    
                    # Уменьшаем длительность и пробуем снова
                    best_end = current_start + (best_end - current_start) * 0.8
                    attempt += 1
                    
                    if attempt >= max_attempts:
                        print(f"   ⚠️  Пропускаем часть {part_num} после {max_attempts} попыток")
                        current_start = best_end
                        break
            
            test_video.close()
            part_num += 1
            
            # Обновляем оценку длительности на основе последнего результата
            if attempt < max_attempts and best_end > current_start:
                chunk_duration = best_end - (current_start - (best_end - current_start))
        
        print("\n" + "=" * 60)
        print("✅ Разбивка завершена успешно!")
        print(f"📁 Все файлы сохранены в: {output_dir}")
        print(f"📦 Создано частей: {part_num - 1}")
        
    except Exception as e:
        print(f"❌ Ошибка при обработке видео: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python video_splitter.py <путь_к_видео> [размер_части_в_МБ]")
        print("Пример: python video_splitter.py video.mp4 200")
        sys.exit(1)
    
    input_file = sys.argv[1]
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    
    split_video(input_file, chunk_size)