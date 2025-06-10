"""
Configuration du bot
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Classe de configuration du bot"""
    
    # Tokens et clés API
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
    TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
    
    # Configuration du bot
    COMMAND_PREFIX = "!"
    BOT_NAME = "DiscTeleBot"
    BOT_VERSION = "1.0.0"
    
    # Paramètres de logging
    LOG_LEVEL = "INFO"
    LOG_TO_FILE = True
    
    # Couleurs pour les embeds
    class Colors:
        PRIMARY = 0x5865F2    # Bleu Discord
        SUCCESS = 0x57F287    # Vert
        WARNING = 0xFEE75C    # Jaune
        ERROR = 0xED4245      # Rouge
        INFO = 0x5865F2       # Bleu
    
    @classmethod
    def validate(cls):
        """Valide la configuration"""
        errors = []
        
        if not cls.DISCORD_TOKEN:
            errors.append("DISCORD_TOKEN manquant dans .env")
        
        if errors:
            raise ValueError("Erreurs de configuration:\n" + "\n".join(f"- {error}" for error in errors))
        
        return True
