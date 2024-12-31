import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import create_embed

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @app_commands.command(name="ping", description="Affiche la latence du bot.")
    async def ping(self, interaction: discord.Interaction):
        """Affiche la latence du bot."""
        latency = round(self.bot.latency * 1000)  # Latence en millisecondes
        embed = create_embed(
            title="Pong!",
            description=f"Latence : {latency} ms",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))