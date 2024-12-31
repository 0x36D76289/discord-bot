import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
import random

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="coinflip", description="Joue à pile ou face.")
    async def coinflip(self, ctx: commands.Context):
        """Joue à pile ou face."""
        result = random.choice(["Pile", "Face"])
        embed = create_embed(
            title="Coinflip",
            description=f"Le résultat est : **{result}**",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Coinflip(bot))