import os
import discord
from discord.ext import commands
from config import Config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
	print(f'{bot.user} has connected to Discord!')
	for cog in os.listdir('./cogs'):
		if cog.endswith('.py'):
			try:
				await bot.load_extension(f'cogs.{cog[:-3]}')
				print(f'Loaded cog: {cog}')
			except Exception as e:
				print(f'Failed to load cog {cog}: {str(e)}')

if __name__ == '__main__':
	token = Config.TOKEN
	print(f"Token type: {type(token)}, Token value: {token[:5]}..." if token else "Token is None")
	bot.run(token)
