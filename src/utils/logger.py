"""
Utilitaires pour le logging
"""
import logging
import sys
from datetime import datetime

def setup_logger(name="DiscTeleBot", level=logging.INFO):
    """Configure et retourne un logger personnalisé"""
    
    # Créer le logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Éviter les doublons si le logger existe déjà
    if logger.handlers:
        return logger
    
    # Format des messages
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Handler pour fichier (optionnel)
    try:
        file_handler = logging.FileHandler(
            f'logs/bot_{datetime.now().strftime("%Y%m%d")}.log',
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (OSError, FileNotFoundError):
        # Si on ne peut pas créer le fichier de log, on continue sans
        pass
    
    logger.addHandler(console_handler)
    
    return logger
