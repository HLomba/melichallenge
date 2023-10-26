# Melichallenge - Proyecto Acortador de URLs 
Este proyecto consiste en un acortador de URLs que transforma URLs largas en URLs cortas, permitiendo agregar, eliminar y verificar la existencia de las mismas y realizar la redireccion a la URL original correspondiente. La solución se encuentra implementada en AWS utilizando servicios Lambda Function y API Gateway y InfinityFree(DNS).

## Funcionalidades
El proyecto ofrece tres APIs principales:

#### 1. challenge-shortURL.py
Esta API permite generar una URL corta a partir de una URL larga utilizando el método POST en la ruta /acortar. Internamente, utiliza una función llamada generate_code.py que genera un código aleatorio de 6 caracteres. Si el código ya existe en la base de datos, se genera uno nuevo hasta que sea único. La URL corta generada se devuelve como respuesta.

#### 2. challenge-rmvURL.py
Esta API permite eliminar una URL acortada, lo que conlleva a la eliminación completa de la asociación entre la URL corta y la URL larga. Se utiliza el método POST en la ruta /rmvurl para realizar esta operación.

#### 3. challenge-redirURL.py
Cuando se ingresa la URL corta en el navegador, esta API está configurada para hacer una redirección 301 a la URL larga correspondiente. La ruta para redirigir está configurada como GET /{short_code}.

### Implementación y Tecnologías
El proyecto está implementado en AWS utilizando servicios Lambda Function y API Gateway. Las rutas de las APIs están configuradas de la siguiente manera:

POST /acortar: Para acortar una URL larga.  
POST /rmvurl: Para eliminar una URL acortada.  
GET /{short_code}: Para redirigir a la URL original utilizando el código corto proporcionado.  

#### Configuración para Redirección
Para lograr la redirección a la URL original, se implementó un subdominio gratuito llamado "infinityfree". Debido a las limitaciones de administración de un dominio gratuito, fue necesario modificar el archivo .htaccess con el siguiente código:
RewriteEngine On
RewriteRule ^(.*)$ https://idendpoint.execute-api.eu-west-1.amazonaws.com/$1 [L,R=301]

Este código permite realizar la redirección de la petición al endpoint del API Gateway, manteniendo el código necesario para obtener y redireccionar correctamente a la URL larga.

### Contenido:
#### challenge-shortURL.py
#### challenge-rmvURL.py
#### challenge-redirURL.py
#### acortadorURL-challenge1 Copy.postman_collection
#### acortadorURL-melichallenge.jpg
