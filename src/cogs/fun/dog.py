import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
import aiohttp

class Dog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="dog", description="Affiche une image de chien aléatoire.")
    async def dog(self, ctx: commands.Context):
        """Affiche une image de chien aléatoire."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thedogapi.com/v1/images/search") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    dog_url = data[0]["url"]
                    embed = create_embed(
                        title="Chien !",
                        color=discord.Color.random(),
                        image=dog_url
                    )
                    await ctx.send(embed=embed)
                else:
                    embed = create_embed(
                        title="Erreur",
                        description="Impossible de récupérer une image de chien pour le moment.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Dog(bot))