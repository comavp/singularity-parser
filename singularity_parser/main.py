import psycopg2
from loguru import logger
from psycopg2 import Error

from backup_files_loader import find_backup_files, BackupFilesNotFoundError, BackupFilesLoadingError

path_to_backup_files = "C:\\Users\\79198\\AppData\\Roaming\\SingularityApp\\nedb-backup"


def create_db_connection():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="12345",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor()
        logger.info(f"Информация о сервере PostgreSql: {connection.get_dsn_parameters()}")
        cursor.execute('SELECT version();')
        record = cursor.fetchone()
        logger.info(f"Вы подключены к - {record}")

    except (Exception, Error) as error:
        logger.error(f"Ошибка при работе с PostgreSql: {str(error)}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info("Соединение с PostgreSQL закрыто")


if __name__ == '__main__':
    try:
        backup_file = find_backup_files(path_to_backup_files)
        logger.info(f"Найден файл {backup_file.name}")
        create_db_connection()
    except BackupFilesNotFoundError as e:
        logger.warning(str(e))
    except BackupFilesLoadingError as e:
        logger.error(str(e))