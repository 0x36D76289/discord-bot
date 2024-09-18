from discord.ext import commands

class UserCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def hello(self, ctx):
		await ctx.send(f'Bonjour {ctx.author.name}!')

async def setup(bot):
	await bot.add_cog(UserCommands(bot))
