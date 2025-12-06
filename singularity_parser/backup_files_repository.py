import psycopg2
from loguru import logger
from psycopg2 import Error


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