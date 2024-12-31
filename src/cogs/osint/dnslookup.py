import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
import dns.resolver

class DNSLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="dnslookup", description="Effectue une recherche DNS pour un nom de domaine.")
    @app_commands.describe(
        domain="Le nom de domaine à rechercher",
        record_type="Le type d'enregistrement DNS (A, MX, CNAME, etc.)"
    )
    async def dnslookup(self, ctx: commands.Context, domain: str, record_type: str = "A"):
        """Effectue une recherche DNS pour un nom de domaine."""
        try:
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(domain, record_type.upper())

            embed = create_embed(
                title=f"Résultats DNS pour {domain} ({record_type.upper()})",
                color=discord.Color.blue()
            )
            results = ""
            for data in answers:
                results += str(data) + "\n"
            embed.add_field(name="Résultats", value=results, inline=False)
            await ctx.send(embed=embed)

        except dns.resolver.NXDOMAIN:
            embed = create_embed(
                title="Erreur",
                description=f"Nom de domaine non trouvé : {domain}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except dns.resolver.NoAnswer:
            embed = create_embed(
                title="Erreur",
                description=f"Aucun enregistrement {record_type.upper()} trouvé pour {domain}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche DNS pour {domain}: {e}")
            embed = create_embed(
                title="Erreur",
                description=f"Une erreur s'est produite lors de la recherche DNS pour {domain}.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DNSLookup(bot))