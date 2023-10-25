import string
import mysql.connector
import json
import logging
from db import get_database_connection

# Configurar el logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        # Conexión a la BD
        conn, cursor = get_database_connection()
        
        # Obtiene el JSON del evento
        data = json.loads(event['body'])
        chameli_url = data.get('short_url')
        print(chameli_url)
        short_code = chameli_url.split('/')[-1]
        print(short_code)

        # Eliminar tupla con short_code de la BD
        cursor.execute('DELETE FROM urls WHERE short_code = %s', (short_code,))
        rows_affected = cursor.rowcount  # Obtener el número de filas afectadas
        conn.commit()  # Commit la transacción

        if rows_affected > 0:
            # Si elimina al menos una fila.
            response = {
                'statusCode': 200,
                'body': json.dumps({'message': 'URL eliminada de la BD: {}'.format(chameli_url)})
            }
        else:
            # No se encontró ninguna URL con el código 
            response = {
                'statusCode': 404,
                'body': json.dumps({'ERROR': 'URL no encontrada en la BD'})
            }

    except mysql.connector.Error as e:
        logger.error("Error de MySQL: %s", str(e))
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error al procesar la solicitud'})
        }

    finally:
        # Cerrar la conexión a la base de datos en caso de error o éxito
        if conn:
            conn.close()
        if cursor:
            cursor.close()

    return response