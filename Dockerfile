# 🐳 Dockerfile para Lucy - Asistente IA con generación de imágenes
FROM python:3.11-slim

# 📦 Instalar dependencias del sistema para PyTorch y PIL
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 📁 Establecer directorio de trabajo
WORKDIR /app

# 📋 Copiar requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# 🔧 Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 📂 Copiar todo el código de la aplicación
COPY . .

# 🌐 Exponer puerto de Streamlit
EXPOSE 8501

# 🚀 Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py", "--server.headless", "true", "--server.address", "0.0.0.0", "--server.port", "8501"]
