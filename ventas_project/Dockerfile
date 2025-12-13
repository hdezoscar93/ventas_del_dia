# Imagen base con Python
FROM python:3.14-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear directorio de la app
WORKDIR /app

# Copiar requirements
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el proyecto
COPY . /app/

# Exponer el puerto
EXPOSE 8000

# Ejecutar migraciones y levantar el servidor con Gunicorn
CMD ["gunicorn", "ventas_project.wsgi:application", "--bind", "0.0.0.0:8000"]
