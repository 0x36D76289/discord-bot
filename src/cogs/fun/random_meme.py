import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from utils.embeds import create_embed

class RandomMeme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="random_meme", description="Affiche un meme aléatoire.", aliases=["meme"])
    async def random_meme(self, ctx: commands.Context):
        """Affiche un meme aléatoire (utilise l'API Reddit)."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    meme_url = data["url"]
                    meme_title = data["title"]
                    meme_author = data["author"]
                    embed = create_embed(
                        title=meme_title,
                        color=discord.Color.random(),
                        image=meme_url,
                        footer=f"Posté par u/{meme_author}"
                    )
                    await ctx.send(embed=embed)
                else:
                    embed = create_embed(
                        title="Erreur",
                        description="Impossible de récupérer un meme pour le moment.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RandomMeme(bot))