from discord.ext import commands

class AdminCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def kick(self, ctx, member: commands.MemberConverter):
		await member.kick()
		await ctx.send(f'{member.name} a été exclu du serveur.')

async def setup(bot):
	await bot.add_cog(AdminCommands(bot))
