import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
from utils.database import clear_warnings

class ClearWarns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="clear_warns", aliases=["clearwarns"], description="Supprime tous les avertissements d'un utilisateur.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(member="Le membre dont vous voulez effacer les avertissements")
    async def clear_warns(self, ctx: commands.Context, member: discord.Member):
        """Supprime tous les avertissements d'un utilisateur."""
        # Supprimez les avertissements de la base de données
        await clear_warnings(member.id, ctx.guild.id)

        embed = create_embed(
            title=f"Avertissements effacés pour {member.name}",
            description=f"Tous les avertissements de {member.mention} ont été effacés.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @clear_warns.error
    async def clear_warns_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            embed = create_embed(
                title="Erreur de permissions",
                description="Vous n'avez pas la permission de supprimer les avertissements des utilisateurs.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ClearWarns(bot))