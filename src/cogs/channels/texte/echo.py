import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="echo", description="Répète le message spécifié.")
    @app_commands.describe(message="Le message à répéter")
    async def echo(self, ctx: commands.Context, *, message: str):
        """Répète le message spécifié."""
        embed = create_embed(
            description=message,
            color=discord.Color.greyple()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Echo(bot))