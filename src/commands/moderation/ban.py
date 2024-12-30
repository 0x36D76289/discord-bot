import discord
from discord.ext import commands
from base_command import BaseCommand

class BanCommand(BaseCommand):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a member from the server."""
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} for {reason}.")