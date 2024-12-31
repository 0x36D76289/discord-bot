import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="avatar", description="Affiche l'avatar d'un utilisateur.")
    @app_commands.describe(member="L'utilisateur dont vous voulez voir l'avatar (optionnel)")
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        """Affiche l'avatar d'un utilisateur."""
        member = member or ctx.author
        embed = create_embed(
            title=f"Avatar de {member}",
            color=discord.Color.blue(),
            image=member.avatar.url
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Avatar(bot))