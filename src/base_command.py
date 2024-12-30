import discord
import logging
from discord.ext import commands

logger = logging.getLogger(__name__)

class BaseCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load(self):
        logger.info(f"Loaded cog: {self.qualified_name}")

    def unload(self):
        logger.info(f"Unloaded cog: {self.qualified_name}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            logger.warning(f"User {ctx.author} tried to use {ctx.command.name} without required permissions.")
            await ctx.send(f"{ctx.author.mention}, you don't have the required permissions to use this command.")

    async def before_invoke(self, ctx):
        logger.info(f"Executing command: {ctx.command.name} by user: {ctx.author}")

    async def after_invoke(self, ctx):
        logger.info(f"Finished executing command: {ctx.command.name}")

    def create_embed(self, title=None, description=None, color=discord.Color.blue(), author=None, thumbnail_url=None, image_url=None, fields=None, footer=None):
        """
        Creates a discord.Embed with the specified parameters.

        Parameters
        ----------
        title : str, optional
            The title of the embed, by default None
        description : str, optional
            The description of the embed, by default None
        color : discord.Color, optional
            The color of the embed, by default discord.Color.blue()
        author : dict, optional
            The author of the embed, by default None. Example: {"name": "Author Name", "url": "https://example.com", "icon_url": "https://example.com/icon.png"}
        thumbnail_url : str, optional
            The thumbnail URL of the embed, by default None
        image_url : str, optional
            The image URL of the embed, by default None
        fields : list, optional
            A list of fields to add to the embed, by default None. Example: [{"name": "Field Name", "value": "Field Value", "inline": True}, ...]
        footer : dict, optional
            The footer of the embed, by default None. Example: {"text": "Footer Text", "icon_url": "https://example.com/icon.png"}

        Returns
        -------
        discord.Embed
            The created embed.
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        if author:
            embed.set_author(name=author.get("name"), url=author.get("url"), icon_url=author.get("icon_url"))

        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)

        if image_url:
            embed.set_image(url=image_url)

        if fields:
            for field in fields:
                embed.add_field(name=field.get("name"), value=field.get("value"), inline=field.get("inline", False))

        if footer:
            embed.set_footer(text=footer.get("text"), icon_url=footer.get("icon_url"))

        return embed