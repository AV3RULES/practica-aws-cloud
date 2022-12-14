# Practica Cloud AWS Avelino

## Diagrama de arquitectura de componentes AWS

![image](https://user-images.githubusercontent.com/31881949/183142161-592ad370-4525-4623-bc48-e8415594c598.png)

### Api Gateway
Se ha escogido esta pieza porque une las funciones y las definiciones de API expuestas al cliente manteniendo las ventajas del modelo serverless.

- import openapi.yaml into https://editor.swagger.io/

*TODO* serverless-openapi-documentation

### Lambda
Igualmente se ha escogido este componente para escribir código python y aprovechar las ventajas de eficiencia y flexibilidad serverless de las funciones lambda. Reciben las llamadas del API y actuan como midleware con la base de datos.

### DynamoDB
Finalmente tenemos este almacenamiento clave-valor: escalado automático en función de la carga de su aplicación, precios de pago por uso, facilidad de inicio y una vez más ausencia de servidores que administrar. Además de su sencilla integración con los componentes anteriores. 

KEY -> ad_id

VALUE -> Ad info y comentarios

## Manual de despliegue

### Requisitos
- cuenta aws
    https://aws.amazon.com/
- usuario iam acceso programatico

- node.js instalado
```console
    sudo apt update
```
```console
    sudo apt install nodejs
```
```console
    node -v
```
    
- npm instalado
```console
    sudo apt install npm
```

### Configuración
- instalar framework de serverless como un modulo global:
```console
    npm install --global serverless
```
- cuenta serverless
```console
    serverless
    serverless config credentials --provider aws --key {aws-iam-programatic-access-user-key} --secret {aws-iam-programatic-access-user-secret} -o
```

### Despliegue
```console
    serverless deploy
```
si la aplicación no existe en serverless dashboard:
```console
    serverless serverless --org=${serverless username}
```

### Uso
- crear y obtener anuncios y comentarios utilizando curl:
```console
    curl -X POST https://XXXXXXX.ads-api.us-east-1.amazonaws.com/ads
```

- utilizando postman:
    ads-api.postman_collection.json

### Borrado
Para eliminar los servicios y todas sus partes
```console
    serverless remove
```
