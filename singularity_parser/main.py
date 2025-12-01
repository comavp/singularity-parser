import os
import json
from loguru import logger

path_to_backup_files = "C:\\Users\\79198\\AppData\\Roaming\\SingularityApp\\nedb-backup"

def find_backup_files(root_dir):
    try:
        all_files = os.listdir(root_dir)
        backup_files = [f for f in all_files if f.endswith('.json') and '.cens' not in f]

        if not backup_files:
            logger.warning(f"В папке {root_dir} не найдено JSON-файлов")

        latest_file_name = max(backup_files, key=lambda x: int(x.split('_')[1]))

        file_path = os.path.join(root_dir, latest_file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"Содержимое файла {latest_file_name}:")
                logger.info(data)
        except FileNotFoundError:
            logger.error(f"Файл не найден: {file_path}")
        except json.JSONDecodeError:
            logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        except UnicodeDecodeError as e:
            logger.error(f"Ошибка кодировки файла {file_path}: {e}")
    except FileNotFoundError:
        logger.error(f"Папка не найдена: {root_dir}")
    except PermissionError:
        logger.error(f"Нет прав доступа к папке: {root_dir}")


if __name__ == '__main__':
    find_backup_files(path_to_backup_files)