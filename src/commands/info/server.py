import discord
from discord.ext import commands
from base_command import BaseCommand

class ServerCommand(BaseCommand):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="serverinfo")
    @commands.guild_only()
    async def server_info(self, ctx):
        """Displays information about the current server."""
        guild = ctx.guild
        fields = [
            {"name": "Name", "value": guild.name, "inline": False},
            {"name": "ID", "value": guild.id, "inline": False},
            {"name": "Owner", "value": guild.owner.mention, "inline": False},
            {"name": "Created At", "value": guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), "inline": False},
            {"name": "Members", "value": guild.member_count, "inline": False},
            {"name": "Roles", "value": len(guild.roles), "inline": False},
            {"name": "Channels", "value": len(guild.text_channels) + len(guild.voice_channels), "inline": False},
            {"name": "Region", "value": str(guild.region), "inline": False},
            {"name": "Verification Level", "value": str(guild.verification_level), "inline": False}
        ]

        embed = self.create_embed(
            title=f"Server Information: {guild.name}",
            color=discord.Color.blue(),
            thumbnail_url=guild.icon.url if guild.icon else None,
            fields=fields
        )
        await ctx.send(embed=embed)
