import discord
from discord.ext import commands
from base_command import BaseCommand

class KickCommand(BaseCommand):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a member from the server."""
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention} for {reason}.")