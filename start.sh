#!/bin/sh

echo "Esperando o banco"

while ! nc -z db 5432; do 
        sleep 0.1
done

echo "Banco foi inicializado"

echo "inicializado Aplicação"

uvicorn main:app --host  0.0.0.0 --proxy-headers --port $APP_PORT_DETALHADOR
