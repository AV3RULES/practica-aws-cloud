# Practica Cloud AWS Avelino

## Diagrama de arquitectura de componentes AWS

![image](https://user-images.githubusercontent.com/31881949/183142161-592ad370-4525-4623-bc48-e8415594c598.png)

### Api Gateway
Se ha escogido esta pieza porque une las funciones y las definiciones de API expuestas al cliente manteniendo las ventajas del modelo serverless.

TODO endpoints/swagger

### Lambda
Igualmente se ha escogido este componente para escribir código python y aprovechar las ventajas de eficiencia y flexibilidad serverless de las funciones lambda. Reciben las llamadas del API y actuan como midleware con la base de datos.

### DynamoDB
Finalmente tenemos este almacenamiento clave-valor: escalado automático en función de la carga de su aplicación, precios de pago por uso, facilidad de inicio y una vez más ausencia de servidores que administrar. Además de su sencilla integración con los componentes anteriores. 

TODO: diseño tablas/PK/Campos

## Manual de despliegue

### Requisitos
cuenta aws
    https://aws.amazon.com/
node.js instalado
    ~/$ sudo apt update
    ~/$ sudo apt install nodejs
    ~/$ node -v
npm instalado
    ~/$ sudo apt install npm

### Configuración
instalar framework de serverless como un modulo global:
    ~/$ npm install --global serverless
cuenta serverless
    ~/$ serverless
    ~/$ serverless config credentials --provider aws --key {aws-iam-programatic-access-user-key} --secret {aws-iam-programatic-access-user-secret} -o

### Despliegue
    ~/$ serverless deploy

### Uso
Crear y obtener anuncios y comentarios utilizando curl:
    ~/$ curl -X POST https://XXXXXXX.ads-api.us-east-1.amazonaws.com/ads

utilizando postman:
    ads-api.postman_collection.json

