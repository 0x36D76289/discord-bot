"""
Bot Discord principal
"""
import os
import sys
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Ajouter le répertoire courant au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports avec gestion d'erreur
try:
    from commands.basic_commands import BasicCommands
    from commands.utility_commands import UtilityCommands  
    from commands.admin_commands import AdminCommands
    from utils.logger import setup_logger
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    sys.exit(1)

# Configuration
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour lire le contenu des messages

class DiscTeleBot(commands.Bot):
    """Classe principale du bot Discord"""
    
    def __init__(self):
        super().__init__(
            command_prefix='!',  # Préfixe pour les commandes traditionnelles
            intents=intents,
            help_command=None  # Désactive la commande help par défaut
        )
        self.logger = setup_logger()
        
    async def setup_hook(self):
        """Configuration initiale du bot"""
        # Ajouter les cogs (modules de commandes)
        await self.add_cog(BasicCommands(self))
        await self.add_cog(UtilityCommands(self))
        await self.add_cog(AdminCommands(self))
        
        # Synchroniser les commandes slash
        try:
            synced = await self.tree.sync()
            self.logger.info(f"Synchronisé {len(synced)} commande(s) slash")
        except Exception as e:
            self.logger.error(f"Erreur lors de la synchronisation: {e}")
    
    async def on_ready(self):
        """Événement déclenché quand le bot est prêt"""
        self.logger.info(f'{self.user} est connecté et prêt!')
        self.logger.info(f'ID du bot: {self.user.id}')
        
        # Afficher les serveurs connectés
        guild_count = len(self.guilds)
        self.logger.info(f'Connecté à {guild_count} serveur(s)')
        
    async def on_command_error(self, ctx, error):
        """Gestion des erreurs de commandes"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore les commandes inexistantes
        
        self.logger.error(f"Erreur de commande: {error}")
        await ctx.send(f"Une erreur s'est produite: {error}")

def run_bot():
    """Lance le bot"""
    logger = setup_logger()
    
    if not TOKEN:
        logger.error("TOKEN Discord manquant dans le fichier .env")
        return
    
    bot = DiscTeleBot()
    bot.run(TOKEN, log_handler=None)  # Utiliser notre propre logger

if __name__ == "__main__":
    run_bot()
