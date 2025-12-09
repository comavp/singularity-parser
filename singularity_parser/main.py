import json

from loguru import logger
import hashlib

from backup_files_loader import find_backup_files, BackupFilesNotFoundError, BackupFilesLoadingError
from singularity_parser.backup_files_repository import DatabaseManager

#path_to_backup_files = "C:\\Users\\79198\\AppData\\Roaming\\SingularityApp\\nedb-backup"
path_to_backup_files = "D:\\PythonProjects\\singularity-parser\\test_backup_files"

MAX_BACKUP_FILES = 5


if __name__ == '__main__':
    try:
        backup_file = find_backup_files(path_to_backup_files)
        file_hash = hashlib.md5(str(backup_file.content).encode()).hexdigest()
        logger.info(f"Найден файл {backup_file.name}, MD5 хэш содержимого: {file_hash}")
        db_manager = DatabaseManager()
        if not db_manager.backup_file_exists(backup_file.name, file_hash):
            db_manager.save_backup_file(backup_file.name, json.dumps(backup_file.content['data']), file_hash)
        db_manager.delete_last_backup_files(MAX_BACKUP_FILES)
    except BackupFilesNotFoundError as e:
        logger.warning(str(e))
    except BackupFilesLoadingError as e:
        logger.error(str(e))