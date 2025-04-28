# Utilise une image officielle Python
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Uvicorn
EXPOSE 8000

# Commande de lancement
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
