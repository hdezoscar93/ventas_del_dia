# Dockerfile en la RAÍZ del repositorio
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar TODO el proyecto
COPY . .

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Puerto
EXPOSE 8000

# Comando para ejecutar
# IMPORTANTE: Ajusta la ruta según tu estructura
CMD ["gunicorn", "ventas_project.wsgi:application", "--bind", "0.0.0.0:8000"]