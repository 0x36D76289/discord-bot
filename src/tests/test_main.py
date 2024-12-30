import unittest
from unittest.mock import AsyncMock, patch
import discord
from discord.ext import commands
from src.main import bot  # Import the bot instance from your main.py
from src.commands.general.ping import PingCommand

class TestBotCommands(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Patch the bot's start method to prevent it from actually connecting to Discord during tests
        self.start_patch = patch('discord.ext.commands.Bot.start')
        self.mock_start = self.start_patch.start()

        # Patch the setup_hook if it's an async method being called outside of the event loop
        self.setup_hook_patch = patch('src.main.setup_hook', new_callable=AsyncMock)
        self.mock_setup_hook = self.setup_hook_patch.start()

        # Create a mock context for testing commands
        self.ctx = AsyncMock(spec=commands.Context)
        self.ctx.author = AsyncMock(spec=discord.Member)
        self.ctx.guild = AsyncMock(spec=discord.Guild)
        self.ctx.channel = AsyncMock(spec=discord.TextChannel)
        self.ctx.message = AsyncMock(spec=discord.Message)
        self.ctx.bot = bot

        # Set up any other necessary mocks or initial conditions here

    async def asyncTearDown(self):
        # Clean up patches
        self.start_patch.stop()
        self.setup_hook_patch.stop()

    async def test_ping_command(self):
        # Instantiate the PingCommand cog
        cog = PingCommand(bot)

        # Manually set the bot attribute if it's not set in your __init__ method
        cog.bot = bot  

        # Simulate invoking the ping command
        await cog.ping(self.ctx)

        # Assert that the bot sends "Pong!" in response
        self.ctx.send.assert_called_once_with("Pong!")

if __name__ == '__main__':
    unittest.main()