import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="join", description="Rejoint le canal vocal de l'auteur.")
    @commands.has_permissions(connect=True, speak=True)
    async def join(self, ctx: commands.Context):
        """Rejoint le canal vocal de l'auteur."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is not None:
                await ctx.voice_client.move_to(channel)
                self.logger.info(f"Le bot a été déplacé vers le canal vocal : {channel.name}")
                embed = create_embed(
                    title="Canal vocal rejoint",
                    description=f"Je me suis déplacé vers le canal vocal : {channel.name}",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                await channel.connect()
                self.logger.info(f"Le bot a rejoint le canal vocal : {channel.name}")
                embed = create_embed(
                    title="Canal vocal rejoint",
                    description=f"J'ai rejoint le canal vocal : {channel.name}",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
        else:
            embed = create_embed(
                title="Erreur",
                description="Vous devez être dans un canal vocal pour utiliser cette commande.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @join.error
    async def join_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            embed = create_embed(
                title="Erreur de permissions",
                description="Je n'ai pas la permission de rejoindre ce canal vocal.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            self.logger.error(f"Erreur lors de la tentative de rejoindre un canal vocal : {error}")
            embed = create_embed(
                title="Erreur",
                description="Une erreur s'est produite en essayant de rejoindre le canal vocal.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Join(bot))