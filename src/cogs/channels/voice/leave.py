import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="leave", description="Quitte le canal vocal.")
    async def leave(self, ctx: commands.Context):
        """Quitte le canal vocal."""
        voice_client = ctx.voice_client
        if voice_client:
            await voice_client.disconnect()
            self.logger.info("Le bot a quitté le canal vocal.")
            embed = create_embed(
                title="Déconnexion",
                description="J'ai quitté le canal vocal.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = create_embed(
                title="Erreur",
                description="Je ne suis pas dans un canal vocal.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leave(bot))