import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
import asyncio

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="play", description="Joue de l'audio à partir d'une URL ou d'un terme de recherche.")
    @app_commands.describe(url="L'URL ou le terme de recherche pour l'audio")
    async def play(self, ctx: commands.Context, *, url: str):
        """Joue de l'audio à partir d'une URL ou d'un terme de recherche.
           (Nécessite youtube-dl ou une bibliothèque similaire)
        """
        if ctx.author.voice is None:
            embed = create_embed(
                title="Erreur",
                description="Vous n'êtes pas connecté à un canal vocal.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        # Utiliser youtube-dl pour obtenir la source audio
        try:
            # Placeholder pour la logique youtube-dl. Remplacer avec votre implémentation réelle.
            # Ceci est un exemple simplifié et pourrait nécessiter des ajustements.
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'default_search': 'auto',
                'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                'restrictfilenames': True,
                'quiet': True,
            }

            import yt_dlp as youtube_dl
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:  # Si c'est une playlist, prendre la première vidéo
                    info = info['entries'][0]
                url2 = info['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'})
                ctx.voice_client.play(source)
                embed = create_embed(
                    title="Lecture en cours",
                    description=f"Lecture : {info.get('title', url)}",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Erreur lors de la lecture audio : {e}")
            embed = create_embed(
                title="Erreur",
                description="Une erreur s'est produite lors de la tentative de lecture de l'audio.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Play(bot))