from discord import app_commands
from discord.ext import commands

class HelpCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name="help", description="Display a list of available commands.")
	async def help(self, interaction: discord.Interaction):
		await interaction.response.send_message("Help command here.")

async def setup(bot):
	await bot.add_cog(HelpCommand(bot))
