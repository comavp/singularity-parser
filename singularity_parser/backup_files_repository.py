import traceback

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

    def save_projects(self, projects_list):
        try:
            cursor = self.__create_cursor()
            for project in projects_list:
                self.save_or_update_project(cursor, project)
            cursor.connection.commit()
            logger.info(f"Проектов сохранено в БД: {len(projects_list)}")
        except (Exception, Error) as error:
            cursor.connection.rollback()
            logger.error(f"Ошибка при работе с PostgreSql: {str(error)}")
        finally:
            cursor.close()
            self.__close_db_connection()

    def save_or_update_project(self, cursor, project):
        select_statement = "SELECT singularity_modificated_date FROM projects WHERE id = %s;"
        cursor.execute(select_statement, (project.id,))
        result = cursor.fetchone()
        if result is None:
            upsert_statement = "INSERT INTO projects (" \
                        "id, title, singularity_created_date, singularity_journal_date, singularity_delete_date, " \
                        "singularity_modificated_date, original_data) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(upsert_statement, (
                project.id,
                project.title,
                project.created_date,
                project.journal_date,
                project.delete_date,
                project.modificated_date,
                project.original_data))
            logger.info(f"Проект '{project.title}' успешно сохранен в БД")
        elif project.modificated_date > int(result[0]):
            upsert_statement = "UPDATE projects SET title = %s, singularity_created_date = %s, " \
                               "singularity_journal_date = %s, singularity_delete_date = %s, " \
                               "singularity_modificated_date = %s, original_data = %s " \
                               "WHERE id = %s;"
            cursor.execute(upsert_statement, (
                project.title,
                project.created_date,
                project.journal_date,
                project.delete_date,
                project.modificated_date,
                project.original_data,
                project.id))
            logger.info(f"Проект '{project.title}' успешно обновлен")

    def save_tasks(self, tasks_list):
        try:
            cursor = self.__create_cursor()
            for task in tasks_list:
                self.save_or_update_task(cursor, task)
            cursor.connection.commit()
            logger.info(f"Задач сохранено в БД: {len(tasks_list)}")
        except (Exception, Error) as error:
            cursor.connection.rollback()
            logger.error(f"Ошибка при работе с PostgreSql: {str(error)}")
        finally:
            cursor.close()
            self.__close_db_connection()

    def save_or_update_task(self, cursor, task):
        select_statement = "SELECT singularity_modificated_date FROM tasks WHERE id = %s"
        cursor.execute(select_statement, (task.id,))
        result = cursor.fetchone()
        if result is None:
            upsert_statement = "INSERT INTO tasks (" \
                        "id, title, singularity_created_date, singularity_journal_date, singularity_delete_date, " \
                        "singularity_modificated_date, original_data, project_id) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(upsert_statement, (
                task.id,
                task.title,
                task.created_date,
                task.journal_date,
                task.delete_date,
                task.modificated_date,
                task.original_data,
                task.project_id))
            logger.info(f"Задача '{task.title}' успешно сохранена в БД")
        elif task.modificated_date > int(result[0]):
            upsert_statement = "UPDATE tasks SET title = %s, singularity_created_date = %s, " \
                               "singularity_journal_date = %s, singularity_delete_date = %s, " \
                               "singularity_modificated_date = %s, original_data = %s " \
                               "WHERE id = %s;"
            cursor.execute(upsert_statement, (
                task.title,
                task.created_date,
                task.journal_date,
                task.delete_date,
                task.modificated_date,
                task.original_data,
                task.id))
            logger.info(f"Задача '{task.title}' успешно обновлена")
