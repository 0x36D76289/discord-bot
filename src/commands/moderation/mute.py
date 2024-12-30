import discord
from discord.ext import commands
from base_command import BaseCommand

class MuteCommand(BaseCommand):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        """Mutes a member in the server."""
        guild = ctx.guild
        mute_role = discord.utils.get(guild.roles, name="Muted")

        if not mute_role:
            mute_role = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)

        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f"Muted {member.mention} for {reason}.")
        
    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmutes a member in the server."""
        guild = ctx.guild
        mute_role = discord.utils.get(guild.roles, name="Muted")

        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"Unmuted {member.mention}.")
        else:
            await ctx.send(f"{member.mention} is not muted.")