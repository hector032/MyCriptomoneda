#Guia de Instalacion local de aplicacion de criptomonedas

1. Instalar todas las dependencias usando el siguiente codigo en el terminal:
    pip install -r requeriments.txt

2. Instalar  el entorno virtual env,
    windows: python -m venv venv
    mac:     python -m venv venv

3. activar entorno virtual env,
    windowns:  venv\scripts\activate
    mac:       . venv/bin/activate

4. duplicar .env_template y renombrar por .env y rellenar los datos necesarios.

4. duplicar config_templates.py y nenombrar por config.py y rellenar los datos necesarios.

5. crea la base de datos con la cual el proyecto funciona,
    create database mycripto.db
    y luego crear las tablas copiando la consulta que esta en la carpeta migrations en el archivo mycripto.sql

6. por ultimo para lanzar la aplicacion debes escribir en la terminarl:
    Flask run