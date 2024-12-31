import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Envoie un message de bienvenue aux nouveaux membres."""
        # Remplacez CHANNEL_ID par l'ID du canal où vous voulez envoyer les messages de bienvenue
        channel = self.bot.get_channel(1232097317411360952)  # Mettez l'ID de votre canal de bienvenue ici
        if channel:
            embed = create_embed(
                title=f"Bienvenue {member.name} !",
                description=f"Bienvenue sur le serveur {member.guild.name} ! N'hésite pas à te présenter.",
                color=discord.Color.random(),
                thumbnail=member.avatar.url if member.avatar else None
            )
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))