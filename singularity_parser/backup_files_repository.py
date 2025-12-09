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
            self.connection = None
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

    def backup_file_exists(self, filename, content_hash):
        try:
            cursor = self.__create_cursor()
            statement = "SELECT bf.id FROM backup_files bf WHERE bf.file_name = %s and bf.hash = %s;"
            cursor.execute(statement, (filename, content_hash))
            result = cursor.fetchone()
            if result:
                logger.info(f"Файл {filename} c хэшем {content_hash} найден в БД")
                return True
            return False
        except (Exception, Error) as error:
            logger.error(f"Ошибка при работе с PostgreSql: {str(error)}")
        finally:
            cursor.close()
            self.__close_db_connection()

    def delete_last_backup_files(self, files_number_to_skip):
        try:
            cursor = self.__create_cursor()
            statement = "SELECT bf.id FROM backup_files bf ORDER BY bf.created_at DESC OFFSET %s;"
            cursor.execute(statement, (str(files_number_to_skip)))
            rows = cursor.fetchall()
            if not rows:
                logger.info(f"Не найдены файлы, которые нужно удалить")
            else:
                ids_to_delete = [str(row[0]) for row in rows]
                cursor.execute("DELETE FROM backup_files WHERE id = ANY(%s::int[]);", (ids_to_delete,))
                cursor.connection.commit()
                logger.info(f"Файлов удалено: {len(ids_to_delete)}")
        except (Exception, Error) as error:
            logger.error(f"Ошибка при работе с PostgreSql: {str(error)}")
            if rows:
                cursor.connection.rollback()
        finally:
            cursor.close()
            self.__close_db_connection()