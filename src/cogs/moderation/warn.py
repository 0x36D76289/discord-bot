import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
from utils.database import add_warning

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="warn", description="Avertit un utilisateur.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        member="Le membre à avertir",
        reason="La raison de l'avertissement"
    )
    async def warn(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Aucune raison spécifiée"):
        """Avertit un utilisateur."""
        # Enregistrez l'avertissement dans la base de données
        await add_warning(member.id, ctx.guild.id, ctx.author.id, reason)

        embed = create_embed(
            title=f"Avertissement pour {member.name}",
            description=f"{member.mention} a été averti pour la raison suivante : {reason}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        # Envoyer un message privé à l'utilisateur averti (facultatif)
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            self.logger.warning(f"Impossible d'envoyer un message privé à {member}")

    @warn.error
    async def warn_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            embed = create_embed(
                title="Erreur de permissions",
                description="Vous n'avez pas la permission d'avertir les utilisateurs.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Warn(bot))