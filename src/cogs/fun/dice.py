import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
import random

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="dice", description="Lance un dé.", aliases=["roll"])
    @app_commands.describe(sides="Le nombre de faces du dé (par défaut : 6)")
    async def dice(self, ctx: commands.Context, sides: int = 6):
        """Lance un dé avec le nombre de faces spécifié (par défaut : 6)."""
        if sides < 2:
            embed = create_embed(
                title="Erreur",
                description="Un dé doit avoir au moins 2 faces.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        result = random.randint(1, sides)
        embed = create_embed(
            title="Lancer de dé",
            description=f"Le résultat est : **{result}**",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Dice(bot))