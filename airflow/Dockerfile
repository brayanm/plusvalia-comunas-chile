FROM apache/airflow:2.9.1

USER root

# Instalar dependencias del sistema necesarias (si es necesario)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && apt-get clean

# Establecer directorio de trabajo
WORKDIR /opt/airflow

# Copiar el archivo requirements.txt
COPY requirements.txt .

# Cambiar al usuario 'airflow' antes de instalar las dependencias
USER airflow

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt