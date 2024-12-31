import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class AddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="add_role", description="Attribue un rôle à un membre.")
    @commands.has_permissions(manage_roles=True)
    @app_commands.describe(
        member="Le membre à qui attribuer le rôle",
        role="Le rôle à attribuer"
    )
    async def add_role(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        """Attribue un rôle à un membre."""
        if role >= ctx.author.top_role:
            embed = create_embed(
                title="Erreur de permissions",
                description="Vous ne pouvez pas attribuer un rôle supérieur ou égal à votre rôle le plus élevé.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if role in member.roles:
            embed = create_embed(
                title="Erreur",
                description=f"{member.mention} a déjà le rôle {role.name}.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        await member.add_roles(role)
        self.logger.info(f"Le rôle {role.name} a été attribué à {member} par {ctx.author}")

        embed = create_embed(
            title="Rôle attribué",
            description=f"Le rôle {role.name} a été attribué à {member.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @add_role.error
    async def add_role_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            embed = create_embed(
                title="Erreur de permissions",
                description="Vous n'avez pas la permission de gérer les rôles.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = create_embed(
                title="Erreur d'argument",
                description="Veuillez spécifier un membre et un rôle valides.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = create_embed(
                title="Erreur",
                description="Il manque des arguments. Veuillez spécifier un membre et un rôle.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AddRole(bot))