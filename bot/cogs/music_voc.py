from discord.ext import commands
import discord
import yt_dlp
import os

class MusicVoc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.voice_client = None
		self.queue = []

	@commands.command()
	async def join(self, ctx):
		if ctx.author.voice:
			channel = ctx.author.voice.channel
			self.voice_client = await channel.connect()
		else:
			await ctx.send("Vous devez être dans un canal vocal pour utiliser cette commande.")

	@commands.command()
	async def leave(self, ctx):
		if self.voice_client:
			await self.voice_client.disconnect()
			self.voice_client = None

	@commands.command()
	async def play(self, ctx, url):
		if not self.voice_client:
			await ctx.send("Je ne suis pas connecté à un canal vocal.")
			return

		ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
			'outtmpl': 'downloads/%(title)s.%(ext)s',
		}

		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			info = ydl.extract_info(url, download=True)
			filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

		self.queue.append(filename)
		await ctx.send(f"Ajouté à la file d'attente: {info['title']}")

		if not self.voice_client.is_playing():
			await self.play_next(ctx)

	async def play_next(self, ctx):
		if self.queue:
			filename = self.queue.pop(0)
			self.voice_client.play(discord.FFmpegPCMAudio(filename), after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
			await ctx.send(f"Lecture en cours: {os.path.basename(filename)}")
		else:
			await ctx.send("La file d'attente est vide.")

async def setup(bot):
	await bot.add_cog(MusicVoc(bot))
