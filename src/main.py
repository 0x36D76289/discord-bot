import os
import discord
import logging
from logging.handlers import RotatingFileHandler
from discord.ext import commands
from dotenv import load_dotenv
from base_command import BaseCommand
from commands.general.ping import PingCommand
from commands.moderation.ban import BanCommand
from commands.moderation.kick import KickCommand
from commands.moderation.mute import MuteCommand
from commands.info.server import ServerCommand
from commands.info.user import UserCommand
from commands.info.invite import InviteCommand

# Load environment variables
load_dotenv()

# Get environment variables
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DEBUG_MODE = os.getenv("DEBUG").lower() == "true"

# Configure logging
def configure_logging():
    log_level = logging.DEBUG if DEBUG_MODE else logging.INFO
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_formatter)

    # File Handler (Rotating)
    file_handler = RotatingFileHandler('discord_bot.log', maxBytes=5*1024*1024, backupCount=5) # 5MB max size, keep 5 backup files
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)

    # Get root logger and add handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    if DEBUG_MODE:
        discord_logger = logging.getLogger('discord')
        discord_logger.setLevel(logging.DEBUG)
        discord_logger.addHandler(console_handler)
        discord_logger.addHandler(file_handler)

configure_logging()
logger = logging.getLogger(__name__)

# Define intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

async def setup_hook():
    await bot.add_cog(PingCommand(bot))
    await bot.add_cog(BanCommand(bot))
    await bot.add_cog(KickCommand(bot))
    await bot.add_cog(MuteCommand(bot))
    await bot.add_cog(ServerCommand(bot))
    await bot.add_cog(UserCommand(bot))
    await bot.add_cog(InviteCommand(bot))

    synced = await bot.tree.sync()
    logger.info(f"Synced {len(synced)} commands with Discord.")


bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name} ({bot.user.id})")

    await bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
    logger.info("Cleared and resynced all commands.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permissions to use this command.")
    else:
        logger.error(f"An error occurred while processing the command '{ctx.command.name if ctx.command else 'unknown'}': {error}", exc_info=True)
        await ctx.send("An error occurred while processing the command.")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)