#imagen madre 
FROM python:3.11-slim   

#CONFIGURACION PARA PODER LOGS DE MANERA CORRECTA
ENV PYTHONBUFFERED=1

# DIRECTORIO DE TRABAJO
WORKDIR /CRUD_django

#copiar archivos de dependencias
COPY requirements.txt  . 

# instala las dependencias via pip 
RUN pip install --no-cache-dir -r requirements.txt
#copiamos codigo fuente del proyecto dentrto de la imagen 
COPY . .
