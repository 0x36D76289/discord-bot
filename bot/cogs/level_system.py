from discord.ext import commands
import random

class LevelSystem(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.user_xp = {}

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return

		user_id = str(message.author.id)
		if user_id not in self.user_xp:
			self.user_xp[user_id] = {'xp': 0, 'level': 1}

		self.user_xp[user_id]['xp'] += random.randint(1, 5)
		if self.user_xp[user_id]['xp'] >= self.user_xp[user_id]['level'] * 100:
			self.user_xp[user_id]['level'] += 1
			await message.channel.send(f'Félicitations {message.author.mention}! Vous avez atteint le niveau {self.user_xp[user_id]["level"]}!')

	@commands.command()
	async def level(self, ctx):
		user_id = str(ctx.author.id)
		if user_id in self.user_xp:
			await ctx.send(f'{ctx.author.name}, vous êtes niveau {self.user_xp[user_id]["level"]} avec {self.user_xp[user_id]["xp"]} XP.')
		else:
			await ctx.send(f'{ctx.author.name}, vous n\'avez pas encore de niveau.')

async def setup(bot):
	await bot.add_cog(LevelSystem(bot))
