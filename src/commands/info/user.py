import discord
from discord.ext import commands
from base_command import BaseCommand

class UserCommand(BaseCommand):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="userinfo")
    async def user_info(self, ctx, user: discord.Member = None):
        """Displays information about a user.

        Parameters
        ----------
        user : discord.Member, optional
            The user to display information about, by default the author of the message.
        """
        if user is None:
            user = ctx.author

        fields = [
            {"name": "Name", "value": user.name, "inline": False},
            {"name": "ID", "value": user.id, "inline": False},
            {"name": "Discriminator", "value": user.discriminator, "inline": False},
            {"name": "Created At", "value": user.created_at.strftime("%Y-%m-%d %H:%M:%S"), "inline": False},
            {"name": "Joined At", "value": user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), "inline": False},
            {"name": "Bot", "value": user.bot, "inline": False},
            {"name": "Status", "value": str(user.status), "inline": False},
            {"name": "Activity", "value": user.activity.name if user.activity else "None", "inline": False},
            {"name": "Roles", "value": ", ".join([role.mention for role in user.roles]), "inline": False}
        ]

        embed = self.create_embed(
            title=f"User Information: {user.name}",
            color=discord.Color.green(),
            thumbnail_url=user.avatar.url if user.avatar else None,
            fields=fields
        )
        await ctx.send(embed=embed)
