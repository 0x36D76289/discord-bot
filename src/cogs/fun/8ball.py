import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
import random

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="8ball", description="Posez une question et la boule 8 magique répondra !")
    @app_commands.describe(question="La question à poser à la boule 8 magique")
    async def eightball(self, ctx: commands.Context, *, question: str):
        """Posez une question et la boule 8 magique répondra !"""
        responses = [
            "C'est certain.",
            "C'est décidément ainsi.",
            "Sans aucun doute.",
            "Oui, absolument.",
            "Tu peux compter dessus.",
            "Comme je le vois, oui.",
            "Très probablement.",
            "Les perspectives sont bonnes.",
            "Oui.",
            "Les signes pointent vers le oui.",
            "Réponse floue, réessayez.",
            "Redemandez plus tard.",
            "Mieux vaut ne pas te le dire maintenant.",
            "Je ne peux pas le prédire maintenant.",
            "Concentrez-vous et demandez à nouveau.",
            "N'y comptez pas.",
            "Ma réponse est non.",
            "Mes sources disent non.",
            "Les perspectives ne sont pas si bonnes.",
            "Très douteux."
        ]
        answer = random.choice(responses)
        embed = create_embed(
            title="Boule 8 magique",
            description=f"**Question :** {question}\n**Réponse :** {answer}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EightBall(bot))