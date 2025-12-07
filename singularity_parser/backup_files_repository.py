import psycopg2
from loguru import logger
from psycopg2 import Error


class DatabaseManager:

    def __init__(self):
        self.connection = None

    def __create_db_connection(self):
        if not self.connection:
            self.connection = psycopg2.connect(user="postgres",
                                          password="12345",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="postgres")
            logger.info(f"Создано соединение с сервером PostgreSql: : {self.connection.get_dsn_parameters()}")
        else:
            logger.info("Будет переиспользовано существующее соединение")

    def __create_cursor(self):
        self.__create_db_connection()
        return self.connection.cursor()

    def __close_db_connection(self):
        if self.connection:
            self.connection.close()
            logger.info("Соединение с PostgreSQL закрыто")

    def save_backup_file(self, filename, content, content_hash):
        try:
            cursor = self.__create_cursor()
            statement = "INSERT INTO backup_files (file_name, data, hash) VALUES (%s, %s, %s);"
            cursor.execute(statement, (filename, content, content_hash))
            cursor.connection.commit()
            logger.info(f"Файл {filename} успешно сохранен в БД")
        except (Exception, Error) as error:
            cursor.connection.rollback()
            logger.error(f"Ошибка при работе с PostgreSql: {str(error)}")
        finally:
            cursor.close()
            self.__close_db_connection()