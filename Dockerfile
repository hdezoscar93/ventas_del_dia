# Imagen base
FROM python:3.14-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar solo el código Django (tu carpeta completa)
COPY ventas_project /app/ventas_project

# Cambiar el directorio de trabajo a donde está manage.py
WORKDIR /app/ventas_project

# Exponer puerto
EXPOSE 8000

# Ejecutar Gunicorn apuntando al WSGI correcto
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ventas_project.wsgi:application"]
