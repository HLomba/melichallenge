import os
import logging
import mysql.connector
from mysql.connector import pooling

# Con figurar el logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Con figurar el pool de conexiones
dbconfig = {
    "host": os.environ.get("DB_host"),
    "user": os.environ.get("DB_user"),
    "password": os.environ.get("DB_passwd"),
    "database": os.environ.get("DB_name")
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)

def get_database_connection():
    try:
        # Conexión a la BD
        conn = connection_pool.get_connection()
        
        if conn:
            cursor = conn.cursor()
            logger.info("Conexión a la base de datos establecida correctamente.")    
            return conn, cursor
        else:
            logger.error("La conexión a la base de datos es None.")
            return None, None

    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return None, None