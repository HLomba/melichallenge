import string
import random
import mysql.connector
import json
import logging
from mysql.connector import pooling
from db import get_database_connection
from generate_code import generate_unique_code
# Configurar el logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        # Conexión a la BD
        conn, cursor = get_database_connection()
        
        # Obtiene el JSON del evento
        data = json.loads(event['body'])
        url = data.get('long_url')

        if url.startswith("http://cha-meli.rf.gd"): 
            code = url.split('/')[-1]
            cursor.execute('SELECT long_url FROM urls WHERE short_code = %s', (code,))
            result = cursor.fetchone()
            logger.info("URL larga obtenida correctamente de la base de datos.")
            print(result)
            if result:
                response = {
                    'statusCode': 200,
                    'body': json.dumps({'message' : f'La URL original es: {result[0]}'})
                }
                return response   
            else:
                response = {
                    'statusCode': 404,
                    'body': json.dumps({'ERROR' : f'No existe una URL larga para: {url}'})
                }
                return response   
        else:    
            cursor.execute('SELECT short_code FROM urls WHERE long_url = %s', (url,))
            result = cursor.fetchone()
            logger.info("URL corta obtenida correctamente de la base de datos.")
            print(result)
            if result:
                code = result[0]
                link = f"http://cha-meli.rf.gd/{code}"  # Reemplaza 'miDominio' con tu dominio personalizado
                response = {
                    'statusCode': 200,
                    'body': json.dumps({'message' : f'La URL corta ya existe, es: {link}'})
                }
                return response
            else:
                short_code = generate_unique_code(cursor)
                # Guardar la asociación en la base de datos
                cursor.execute('INSERT INTO urls (short_code, long_url) VALUES (%s, %s)', (short_code, url))
                conn.commit()
                logger.info("URL corta creada correctamente en la base de datos.")
            
                # Construir la URL corta
                shortened_url = f"http://cha-meli.rf.gd/{short_code}"  # dominio personalizado
                    
                # Devolver la respuesta con la URL corta generada
                response = {
                    'statusCode': 200,
                    'body': json.dumps({'message' : f'URL corta generada correctamente: {shortened_url}'})
                }

    except Exception as e:
        logger.error("Error: %s", str(e))
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error al procesar la solicitud'})
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return response