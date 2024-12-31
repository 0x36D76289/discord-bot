import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
from cogs.osint.reverse_service.yandex_service import YandexService
import aiohttp
from bs4 import BeautifulSoup
import re

class ReverseImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="reverse", description="Effectue une recherche inversée d'une image ou d'une vidéo.")
    @app_commands.describe(
        image_url="L'URL de l'image ou de la vidéo à rechercher",
        file="Le fichier image ou vidéo à rechercher",
        service="Le service de recherche inversée à utiliser (google, yandex)"
    )
    @app_commands.choices(service=[
        app_commands.Choice(name="Google Images", value="google"),
        app_commands.Choice(name="Yandex Images", value="yandex"),
    ])
    async def reverse(self, ctx: commands.Context, service: str, image_url: str = None, file: discord.Attachment = None):
        """Effectue une recherche inversée d'une image ou d'une vidéo."""
        await ctx.defer()

        if not image_url and not file:
            embed = create_embed(
                title="Erreur",
                description="Veuillez fournir une URL d'image ou un fichier.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if image_url and file:
            embed = create_embed(
                title="Erreur",
                description="Veuillez fournir soit une URL d'image, soit un fichier, mais pas les deux.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            if service == "google":
                service_instance = GoogleService()
            elif service == "yandex":
                service_instance = YandexService()
            else:
                embed = create_embed(
                    title="Erreur",
                    description="Service de recherche inversée non reconnu.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            if file:
                image_url = file.url
                file = None
            
            results = await service_instance.search_image(image_url=image_url)

            if results:
                embed = create_embed(
                    title="Résultats de la recherche inversée",
                    color=discord.Color.blue()
                )
                for result in results:
                    if result["service"] == "Google Images":
                        embed.add_field(name="Résultat Google Images", value=f"[Lien vers l'image]({result['url']})\n[Page source]({result['page_url']})", inline=False)
                    elif result["service"] == "Yandex Images":
                        embed.add_field(name="Résultat Yandex Images", value=f"[Lien vers l'image]({result['url']})\n[Page source]({result['page_url']})", inline=False)

                await ctx.send(embed=embed)
            else:
                embed = create_embed(
                    title="Résultats de la recherche inversée",
                    description="Aucun résultat trouvé.",
                    color=discord.Color.yellow()
                )
                await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche inversée : {e}")
            embed = create_embed(
                title="Erreur",
                description="Une erreur s'est produite lors de la recherche inversée.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ReverseImage(bot))

class GoogleService:
    def __init__(self):
        self.base_url = "https://www.google.com/searchbyimage"

    async def search_image(self, image_url=None, filepath=None):
        
        url = f"{self.base_url}?q={}