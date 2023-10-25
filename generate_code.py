import string
import random
import mysql.connector
import logging
from mysql.connector import pooling

# Configurar el logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def generate_random_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def code_exists_in_database(code, cursor):
    # Realiza una consulta para verificar si el código existe en la base de datos
    cursor.execute('SELECT COUNT(*) FROM urls WHERE short_code = %s', (code,))
    #cursor.execute(query, (code,))
    result = cursor.fetchone()
    return result[0] > 0

def generate_unique_code(cursor):
    while True:
        # Genera un código aleatorio
        code = generate_random_code()

        # Verifica si el código ya existe en la base de datos
        if not code_exists_in_database(code, cursor):
            # Si el código no existe, retorna el código único
            return code