import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="purge", description="Supprime un nombre spécifié de messages.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        amount="Le nombre de messages à supprimer"
    )
    async def purge(self, ctx: commands.Context, amount: int):
        """Supprime un nombre spécifié de messages dans le canal actuel."""
        self.logger.debug(f"Commande purge appelée avec amount={amount}")
        await ctx.channel.purge(limit=amount + 1)  # +1 pour inclure la commande elle-même
        self.logger.info(f"{amount} messages ont été supprimés dans {ctx.channel.name} par {ctx.author}")

        embed = create_embed(
            title="Messages supprimés",
            description=f"{amount} messages ont été supprimés.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed, delete_after=5)
        self.logger.debug("Message de confirmation envoyé")

    @purge.error
    async def purge_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            embed = create_embed(
                title="Erreur de permissions",
                description="Vous n'avez pas la permission de gérer les messages.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = create_embed(
                title="Erreur d'argument",
                description="Veuillez spécifier un nombre entier de messages à supprimer.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        self.logger.error(f"Erreur lors de l'exécution de la commande purge: {error}")

async def setup(bot):
    await bot.add_cog(Purge(bot))