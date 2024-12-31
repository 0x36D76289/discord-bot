import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="kick", description="Expulse un membre du serveur.")
    @commands.has_permissions(kick_members=True)
    @app_commands.describe(
        member="Le membre à expulser",
        reason="La raison de l'expulsion"
    )
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        """Expulse un membre du serveur."""
        await member.kick(reason=reason)
        self.logger.info(f"{member} a été expulsé par {ctx.author} pour la raison : {reason}")

        embed = create_embed(
            title="Membre expulsé",
            description=f"{member} a été expulsé.",
            color=discord.Color.orange(),
            fields=[
                {"name": "Raison", "value": reason or "Aucune raison spécifiée", "inline": False},
                {"name": "Expulsé par", "value": ctx.author.mention, "inline": False}
            ]
        )
        await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            embed = create_embed(
                title="Erreur de permissions",
                description="Vous n'avez pas la permission d'expulser des membres.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Kick(bot))