# Usar imagen oficial de Python 3.13
FROM python:3.13-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar uv para gestión de dependencias más rápida
RUN pip install uv

# Copiar archivos de configuración
COPY pyproject.toml uv.lock ./

# Copiar todo el código fuente (incluyendo app/ y main.py)
COPY . .

# Instalar dependencias
RUN uv sync --frozen

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Exponer puerto
EXPOSE 8000

# Variables de entorno por defecto
ENV KAFKA_ENABLED=true
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# Comando para ejecutar la aplicación
CMD ["uv", "run", "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 