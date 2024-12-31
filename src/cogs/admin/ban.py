import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="ban", description="Bannit un membre du serveur.")
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(
        member="Le membre à bannir",
        reason="La raison du bannissement"
    )
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        """Bannit un membre du serveur."""
        await member.ban(reason=reason)
        self.logger.info(f"{member} a été banni par {ctx.author} pour la raison : {reason}")

        embed = create_embed(
            title="Membre banni",
            description=f"{member} a été banni.",
            color=discord.Color.red(),
            fields=[
                {"name": "Raison", "value": reason or "Aucune raison spécifiée", "inline": False},
                {"name": "Banni par", "value": ctx.author.mention, "inline": False}
            ]
        )
        await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            embed = create_embed(
                title="Erreur de permissions",
                description="Vous n'avez pas la permission de bannir des membres.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ban(bot))