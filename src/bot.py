import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger()

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

class MyBot(commands.Bot):
    def __init__(self, intents):
        super().__init__(intents=intents, command_prefix="/")
        self.logger = logger

    async def setup_hook(self):
        self.remove_command('help')

        # Load cogs manually
        initial_extensions = [
            'cogs.admin.ban',
            'cogs.admin.kick',
            'cogs.admin.purge',
            'cogs.admin.serverinfo',
            'cogs.channels.texte.echo',
            'cogs.channels.texte.poll',
            'cogs.channels.voice.join',
            'cogs.channels.voice.leave',
            'cogs.channels.voice.play',
            # 'cogs.channels.voice.queue', # (à compléter plus tard)
            'cogs.fun.coinflip',
            'cogs.fun.dice',
            'cogs.fun.random_meme',
            'cogs.fun.8ball',
            'cogs.fun.cat',
            'cogs.fun.dog',
            'cogs.moderation.add_role',
            'cogs.moderation.remove_role',
            'cogs.moderation.warn',
            'cogs.moderation.warnings',
            'cogs.moderation.clear_warns',
            'cogs.osint.whois',
            'cogs.osint.dnslookup',
            'cogs.osint.reverse',
            'cogs.utils.fxtwitter',
            'cogs.utils.avatar',
            'cogs.utils.help',
            'cogs.utils.ping',
            'cogs.utils.telegram_handler',
            'cogs.welcome.welcome'
        ]
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                # self.logger.info(f"Cog loaded: {extension}")
            except Exception as e:
                self.logger.error(f"Failed to load cog {extension}: {e}")

        # Sync commands with Discord
        if GUILD_ID:
            # Guild-specific commands (for testing)
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            self.logger.info(f"Commands synced with guild {GUILD_ID}")
        else:
            # Global commands (might take up to an hour to update)
            await self.tree.sync()
            self.logger.info("Global commands synced")

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user.name} ({self.user.id})")

    async def on_command(self, ctx: commands.Context):
        """Log command usage."""
        self.logger.info(f"Command executed: {ctx.command} by {ctx.author} in {ctx.channel} (Guild: {ctx.guild})")

    async def on_command_error(self, ctx: commands.Context, error):
        """Log command errors."""
        self.logger.error(f"Error in command {ctx.command}: {error}")

# Configure intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

# Create bot instance
bot = MyBot(intents=intents)

# Run the bot
if __name__ == "__main__":
    if TOKEN is None:
        logger.error("DISCORD_TOKEN not found in .env file.")
    else:
        bot.run(TOKEN)