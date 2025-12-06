from loguru import logger

from backup_files_loader import find_backup_files, BackupFilesNotFoundError, BackupFilesLoadingError
from singularity_parser.backup_files_repository import create_db_connection

path_to_backup_files = "C:\\Users\\79198\\AppData\\Roaming\\SingularityApp\\nedb-backup"


if __name__ == '__main__':
    try:
        backup_file = find_backup_files(path_to_backup_files)
        logger.info(f"Найден файл {backup_file.name}")
        create_db_connection()
    except BackupFilesNotFoundError as e:
        logger.warning(str(e))
    except BackupFilesLoadingError as e:
        logger.error(str(e))