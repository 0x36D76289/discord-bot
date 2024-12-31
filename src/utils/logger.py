import logging
import sys

def setup_logger():
    """Configure le logger pour le bot."""
    logger = logging.getLogger("discord_bot")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler pour écrire dans un fichier (optionnel)
    # file_handler = logging.FileHandler('discord_bot.log')
    # file_handler.setLevel(logging.DEBUG)
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    return logger