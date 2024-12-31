import discord
from discord.ext import commands
from utils.embeds import create_embed

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="serverinfo", description="Affiche des informations sur le serveur.", aliases=["server", "guildinfo"])
    async def serverinfo(self, ctx: commands.Context):
        """Affiche des informations sur le serveur."""
        guild = ctx.guild
        embed = create_embed(
            title=f"Informations sur {guild.name}",
            color=discord.Color.blue(),
            thumbnail=guild.icon.url if guild.icon else None,
            fields=[
                {"name": "ID", "value": guild.id, "inline": True},
                {"name": "Propriétaire", "value": guild.owner.mention, "inline": True},
                {"name": "Langue préférée", "value": guild.preferred_locale, "inline": True},
                {"name": "Membres", "value": guild.member_count, "inline": True},
                {"name": "Canaux textuels", "value": len(guild.text_channels), "inline": True},
                {"name": "Canaux vocaux", "value": len(guild.voice_channels), "inline": True},
                {"name": "Rôles", "value": len(guild.roles), "inline": True},
                {"name": "Date de création", "value": guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), "inline": False}
            ]
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))