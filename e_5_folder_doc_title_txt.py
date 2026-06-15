import os

def create_txt_files_recursively():
    # Путь к основной папке
    base_path = "/Volumes/Macintosh HD — данные/Users/mac/Downloads/!Edu/Janetakis/[Udemy] [Nick Janetakis] Docker для DevOps от разработки до продакшена (2025)/en"
    
    # Проверяем, существует ли основная папка
    if not os.path.exists(base_path):
        print(f"Ошибка: Папка '{base_path}' не найдена!")
        return
    
    created_files = 0
    
    def create_txt_in_directory(directory_path):
        """Создает txt файл в указанной директории"""
        nonlocal created_files
        
        # Получаем название папки
        folder_name = os.path.basename(directory_path)
        if not folder_name:  # Для корневой папки
            folder_name = "root"
        
        # Создаем имя файла
        txt_filename = f"_{folder_name}.txt"
        txt_filepath = os.path.join(directory_path, txt_filename)
        
        try:
            # Создаем txt файл
            with open(txt_filepath, 'w', encoding='utf-8') as f:
                f.write(f"Файл для папки: {folder_name}\n")
                f.write(f"Путь: {directory_path}\n")
                f.write(f"Создан автоматически\n")
            
            print(f"Создан файл: {txt_filepath}")
            created_files += 1
            
        except PermissionError:
            print(f"Ошибка: Нет прав для создания файла '{txt_filename}' в папке '{directory_path}'")
        except Exception as e:
            print(f"Ошибка при создании файла '{txt_filename}' в '{directory_path}': {e}")
    
    # Создаем файл в корневой папке
    create_txt_in_directory(base_path)
    
    # Рекурсивно проходим по всем подпапкам
    try:
        for root, dirs, files in os.walk(base_path):
            # Пропускаем корневую папку, так как уже обработали её
            if root == base_path:
                continue
            
            # Создаем файл в текущей папке
            create_txt_in_directory(root)
            
    except PermissionError:
        print(f"Ошибка: Нет доступа к некоторым папкам в '{base_path}'")
    except Exception as e:
        print(f"Ошибка при обходе папок: {e}")
    
    print(f"\nВсего создано файлов: {created_files}")

if __name__ == "__main__":
    create_txt_files_recursively()