import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
from utils.database import get_warnings

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="warnings", description="Affiche les avertissements d'un utilisateur.")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(member="Le membre dont vous voulez voir les avertissements")
    async def warnings(self, ctx: commands.Context, member: discord.Member):
        """Affiche les avertissements d'un utilisateur."""
        # Récupérez les avertissements depuis la base de données
        warnings = await get_warnings(member.id, ctx.guild.id)

        if not warnings:
            embed = create_embed(
                title=f"Avertissements pour {member.name}",
                description=f"{member.mention} n'a aucun avertissement.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return

        embed = create_embed(
            title=f"Avertissements pour {member.name}",
            color=discord.Color.orange()
        )
        for i, warning in enumerate(warnings):
            warn_id, warner_id, reason, date = warning
            warner = ctx.guild.get_member(warner_id)
            embed.add_field(
                name=f"Avertissement #{i+1}",
                value=f"**Raison :** {reason}\n"
                      f"**Averti par :** {warner.mention if warner else 'Utilisateur inconnu'} ({warner_id})\n"
                      f"**Date :** {date.strftime('%d/%m/%Y %H:%M')}",
                inline=False
            )

        await ctx.send(embed=embed)

    @warnings.error
    async def warnings_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            embed = create_embed(
                title="Erreur de permissions",
                description="Vous n'avez pas la permission de voir les avertissements des utilisateurs.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Warnings(bot))