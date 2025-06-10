"""
Point d'entrée principal du bot Discord
"""
from bot import run_bot
from config import Config
from utils.logger import setup_logger

def main():
    """Fonction principale"""
    logger = setup_logger()
    
    try:
        # Valider la configuration
        Config.validate()
        logger.info("Configuration validée avec succès")
        
        # Lancer le bot
        logger.info("Démarrage du bot...")
        run_bot()
        
    except ValueError as e:
        logger.error(f"Erreur de configuration: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Arrêt du bot demandé par l'utilisateur")
        return 0
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    exit(main())