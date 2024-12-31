import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class GoogleDorks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="dorks", aliases=["google_dorks"], description="Aide à la construction de requêtes Google Dorks.")
    @app_commands.describe(
        query="La requête de recherche",
        site="Le site à cibler (facultatif)",
        filetype="Le type de fichier à rechercher (facultatif)",
        inurl="Un motif à rechercher dans l'URL (facultatif)",
        intitle="Un motif à rechercher dans le titre (facultatif)",
        intext="Un motif à rechercher dans le texte (facultatif)"
    )
    async def dorks(self, ctx: commands.Context, query: str, site: str = None, filetype: str = None, inurl: str = None, intitle: str = None, intext: str = None):
        """Aide à la construction de requêtes Google Dorks."""
        dork = query
        if site:
            dork += f" site:{site}"
        if filetype:
            dork += f" filetype:{filetype}"
        if inurl:
            dork += f" inurl:{inurl}"
        if intitle:
            dork += f" intitle:{intitle}"
        if intext:
            dork += f" intext:{intext}"

        google_link = f"https://www.google.com/search?q={dork.replace(' ', '+')}"

        embed = create_embed(
            title="Google Dork",
            description=f"**Requête :** `{dork}`\n[Lien vers la recherche Google]({google_link})",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GoogleDorks(bot))