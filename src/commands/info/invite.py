import discord
import validators
from discord.ext import commands
from base_command import BaseCommand

class InviteCommand(BaseCommand):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="inviteinfo")
    async def invite_info(self, ctx, invite_link: str):
        """Displays information about a Discord invite.

        Parameters
        ----------
        invite_link : str
            The invite link to display information about.
        """

        if not validators.url(invite_link):
            await ctx.send("Invalid invite link.")
            return

        try:
            invite = await self.bot.fetch_invite(invite_link)
        except discord.NotFound:
            await ctx.send("Invite not found.")
            return
        except discord.HTTPException:
            await ctx.send("An error occurred while fetching the invite.")
            return

        fields = []
        if invite.guild:
            fields.extend([
                {"name": "Server Name", "value": invite.guild.name, "inline": False},
                {"name": "Server ID", "value": invite.guild.id, "inline": False}
            ])
        if invite.channel:
            fields.append({"name": "Channel Name", "value": invite.channel.name, "inline": False})
        if invite.inviter:
            fields.append({"name": "Inviter", "value": invite.inviter.mention, "inline": False})

        fields.extend([
            {"name": "Uses", "value": invite.uses, "inline": False},
            {"name": "Max Uses", "value": invite.max_uses, "inline": False},
            {"name": "Temporary", "value": invite.temporary, "inline": False},
            {"name": "Created At", "value": invite.created_at.strftime("%Y-%m-%d %H:%M:%S"), "inline": False}
        ])

        embed = self.create_embed(
            title=f"Invite Information: {invite.code}",
            color=discord.Color.orange(),
            thumbnail_url=invite.guild.icon.url if invite.guild and invite.guild.icon else None,
            fields=fields
        )
        await ctx.send(embed=embed)
