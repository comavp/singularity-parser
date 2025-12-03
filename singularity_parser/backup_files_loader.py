import os
import json


class BackupFilesNotFoundError(Exception):
    """Ошибка в случае, если не найден ни один файл в заданной директории"""
    pass


class BackupFilesLoadingError(Exception):
    """Ошибка в случае, если проиозшла проблема при загрузке файлов"""
    pass


class BackupFile:

    def __init__(self, name, content):
        self.name = name
        self.content = content


def find_backup_files(root_dir):
    try:
        all_files = os.listdir(root_dir)
        backup_files = [f for f in all_files if f.endswith('.json') and '.cens' not in f and '_' in f]

        if not backup_files:
            raise BackupFilesNotFoundError(f"В папке {root_dir} не найдено JSON-файлов")

        latest_file_name = max(backup_files, key=lambda x: int(x.split('_')[1]))

        file_path = os.path.join(root_dir, latest_file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return BackupFile(latest_file_name, json.load(file))
        except FileNotFoundError as e:
            raise BackupFilesLoadingError(f"Файл не найден: {file_path}") from e
        except json.JSONDecodeError as e:
            raise BackupFilesLoadingError(f"Ошибка декодирования JSON в файле: {file_path}") from e
        except UnicodeDecodeError as e:
            raise BackupFilesLoadingError(f"Ошибка кодировки файла {file_path}: {e}") from e
    except FileNotFoundError as e:
        raise BackupFilesLoadingError(f"Папка не найдена: {root_dir}") from e
    except PermissionError as e:
        raise BackupFilesLoadingError(f"Нет прав доступа к папке: {root_dir}") from e