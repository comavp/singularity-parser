from backup_files_loader import find_backup_files, BackupFilesNotFoundError, BackupFilesLoadingError
from loguru import logger

path_to_backup_files = "C:\\Users\\79198\\AppData\\Roaming\\SingularityApp\\nedb-backup"

if __name__ == '__main__':
    try:
        backup_file = find_backup_files(path_to_backup_files)
        logger.info(f"Содержимое файла {backup_file.name}:")
        logger.info(backup_file.content)
    except BackupFilesNotFoundError as e:
        logger.warning(str(e))
    except BackupFilesLoadingError as e:
        logger.error(str(e))