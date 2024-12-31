import discord
from discord.ext import commands
import re

class FixTweet(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.logger = bot.logger
		self.twitter_regex = re.compile(r"https?://(?:www\.)?twitter\.com/(\w+)/status/(\d+)")

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return

		match = self.twitter_regex.search(message.content)
		if match:
			username = match.group(1)
			tweet_id = match.group(2)
			fxtweet_link = f"https://fxtwitter.com/{username}/status/{tweet_id}"

			if len(fxtweet_link) > 280:
				fxtweet_link = fxtweet_link[:-3] + "..."

			await message.channel.send(f"{message.author.mention} a partagé un lien Twitter, voici la version FixTweet : {fxtweet_link}")
			await message.edit(suppress=True) # Supprimer l'embed original du tweet

async def setup(bot):
	await bot.add_cog(FixTweet(bot))