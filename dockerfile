# Usa una imagen oficial de Python como imagen padre
FROM python:3.10-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala las dependencias del sistema necesarias
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el proyecto
COPY . .

# Expone el puerto en el que se ejecutará la aplicación Django
EXPOSE 8000

# Comando para ejecutar la aplicación. Cambia `myproject` al nombre de tu módulo de proyecto Django.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]