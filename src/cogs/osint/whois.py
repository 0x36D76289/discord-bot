import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
import whois

class Whois(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="whois", description="Effectue une recherche Whois sur un nom de domaine.")
    @app_commands.describe(domain="Le nom de domaine à rechercher")
    async def whois(self, ctx: commands.Context, domain: str):
        """Effectue une recherche Whois sur un nom de domaine."""
        try:
            w = whois.whois(domain)
            if w:
                embed = create_embed(
                    title=f"Whois pour {domain}",
                    color=discord.Color.blue()
                )
                # Ajouter les champs pertinents du résultat Whois
                if w.registrar:
                    embed.add_field(name="Registrar", value=w.registrar, inline=False)
                if w.creation_date:
                    embed.add_field(name="Date de création", value=str(w.creation_date), inline=False)
                if w.expiration_date:
                    embed.add_field(name="Date d'expiration", value=str(w.expiration_date), inline=False)
                if w.name_servers:
                    embed.add_field(name="Serveurs de noms", value=", ".join(w.name_servers), inline=False)
                if w.text:
                    # Limiter la taille du champ 'Données brutes' pour éviter de dépasser la limite de Discord
                    if len(w.text) > 1024:
                        raw_data = w.text[:1021] + "..."
                    else:
                        raw_data = w.text
                    embed.add_field(name="Données brutes", value=raw_data, inline=False)

                await ctx.send(embed=embed)
            else:
                embed = create_embed(
                    title=f"Whois pour {domain}",
                    description="Aucune information Whois trouvée.",
                    color=discord.Color.yellow()
                )
                await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche Whois pour {domain}: {e}")
            embed = create_embed(
                title="Erreur",
                description=f"Une erreur s'est produite lors de la recherche Whois pour {domain}.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Whois(bot))