FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/

# Créer le dossier logs
RUN mkdir -p logs

# Exposer le port (pas nécessaire pour un bot Discord, mais utile pour des webhooks futurs)
EXPOSE 8000

# Commande de démarrage
CMD ["python", "src/main.py"]
