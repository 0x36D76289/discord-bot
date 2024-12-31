import discord
from discord.ext import commands
import re
from pyrogram import Client
from pyrogram.errors import BadRequest
from utils.embeds import create_embed
import os

TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class TelegramHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.telegram_regex = re.compile(r"https?://(?:www\.)?(?:t|telegram)\.me/([a-zA-Z0-9_]{5,32})/(?:\d+)")
        self.channel_regex = re.compile(r"https?://(?:www\.)?(?:t|telegram)\.me/c/(\d+)/(\d+)")

        self.api_id = TELEGRAM_API_ID
        self.api_hash = TELEGRAM_API_HASH
        self.bot_token = TELEGRAM_BOT_TOKEN

        self.pyrogram_client = Client(
            "discord_bot",
            api_id=self.api_id,
            api_hash=self.api_hash,
            bot_token=self.bot_token,
        )

    async def resolve_channel_link(self, group_id, message_id):
        async with self.pyrogram_client:
            full_id = int(f"-100{group_id}")
            try:
                message = await self.pyrogram_client.get_messages(full_id, int(message_id))
            except:
                return None
            
            return message

    async def resolve_username_link(self, username, message_id):
        async with self.pyrogram_client:
            try:
                message = await self.pyrogram_client.get_messages(username, int(message_id))
            except:
                return None

            return message

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        match_channel = self.channel_regex.search(message.content)
        match_username = self.telegram_regex.search(message.content)

        if match_channel:
            group_id = match_channel.group(1)
            message_id = match_channel.group(2)
            
            telegram_message = await self.resolve_channel_link(group_id, message_id)

        elif match_username:
            username = match_username.group(1)
            message_id = match_username.group(2)
            
            telegram_message = await self.resolve_username_link(username, message_id)

        else: return

        if telegram_message:
            if telegram_message.text:
                content = telegram_message.text
            elif telegram_message.caption:
                content = telegram_message.caption
            else:
                content = "Pas de text"

            embed = create_embed(
                title=f"Message Telegram",
                description=f"{content}\n\n[Lien vers le message]({message.content})",
                color=discord.Color.blue(),
                footer="Stats du message",
                url=message.content
            )

            if telegram_message.photo:
                embed.set_image(url=telegram_message.photo.file_id)

            await message.channel.send(embed=embed)
            await message.edit(suppress=True)

async def setup(bot):
    cog = TelegramHandler(bot)
    await bot.add_cog(cog)