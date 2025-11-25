FROM python:3.11-slim

#Directorio de trabajo
WORKDIR /app

#Copiar archivos necesarios
COPY requirements.txt .

#Instalar Dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto de la app FastAPI
EXPOSE 8082

# Comando para iniciar tu aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8082"]