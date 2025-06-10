#!/bin/bash
# Script de démarrage du bot Discord

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🤖 Démarrage du DiscTeleBot${NC}"
echo "======================================"

# Vérifier que l'environnement virtuel existe
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Environnement virtuel manquant${NC}"
    echo -e "${YELLOW}Création de l'environnement virtuel...${NC}"
    python3 -m venv .venv
fi

# Installer/mettre à jour les dépendances
echo -e "${YELLOW}📦 Installation des dépendances...${NC}"
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# Vérifier que le fichier .env existe
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Fichier .env manquant${NC}"
    echo -e "${YELLOW}Veuillez créer un fichier .env avec votre DISCORD_TOKEN${NC}"
    exit 1
fi

# Créer le dossier logs s'il n'existe pas
mkdir -p logs

# Démarrer le bot
echo -e "${GREEN}🚀 Lancement du bot...${NC}"
echo "======================================"
.venv/bin/python src/main.py