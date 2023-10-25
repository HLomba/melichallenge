import string
import mysql.connector
import json
import logging
#from mysql.connector import pooling
from db import get_database_connection

# Configurar el logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Conexión a la BD
        conn, cursor = get_database_connection()
        
        # Obtiene el JSON del evento
        short_code = event.get('pathParameters', {}).get('short_code', '')
        print(short_code)

        # Consulta si existe la URL corta
        cursor.execute('SELECT long_url FROM urls WHERE short_code = %s', (short_code,))
        result = cursor.fetchone()
        logger.info("URL larga obtenida correctamente de la base de datos.")
        print (result)
        if result:
            long_url = result[0]
            # Realizar la redirección a long_url
            return {
                'statusCode': 301,  # 301 indica una redirección permanente
                'headers': {
                    'Location': long_url
                }
            }
        else:
            # Manejar el caso cuando no se encuentra el código
            return {
                'statusCode': 404,
                'body': json.dumps({'ERROR' : f'En la BD, No existe la URL corta: http://cha-meli.rf.gd/{short_code}'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()