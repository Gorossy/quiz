FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala las herramientas de compilación y otros paquetes esenciales
RUN apt-get update && apt-get install -y \
    build-essential \
    libc6-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip
RUN pip install --upgrade pip

# Instala las dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el proyecto
COPY . .

# Expone el puerto en el que se ejecutará la aplicación Django
EXPOSE 8000

# Comando para ejecutar la aplicación. Cambia `myproject` al nombre de tu módulo de proyecto Django.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]