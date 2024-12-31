import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed
import asyncio

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="poll", description="Crée un sondage avec plusieurs options.")
    @app_commands.describe(
        question="La question du sondage",
        option1="Option 1",
        option2="Option 2",
        option3="Option 3 (facultatif)",
        option4="Option 4 (facultatif)",
        option5="Option 5 (facultatif)",
        option6="Option 6 (facultatif)",
        option7="Option 7 (facultatif)",
        option8="Option 8 (facultatif)",
        option9="Option 9 (facultatif)",
        duration="Durée du sondage en secondes (par défaut: 60)"
    )
    async def poll(self, ctx: commands.Context, question: str, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None, option6: str = None, option7: str = None, option8: str = None, option9: str = None, duration: int = 60):
        """Crée un sondage avec plusieurs options.

        Utilisation: /poll "Question" "Option 1" "Option 2" "Option 3" ... [durée en secondes]
        """
        options = [option1, option2, option3, option4, option5, option6, option7, option8, option9]
        options = [option for option in options if option is not None]

        if len(options) < 2:
            embed = create_embed(
                title="Erreur de syntaxe",
                description="Un sondage doit avoir au moins 2 options.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        if len(options) > 9:
            embed = create_embed(
                title="Erreur de syntaxe",
                description="Un sondage ne peut pas avoir plus de 9 options.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        description = ""
        for i, option in enumerate(options):
            description += f"{reactions[i]} {option}\n"
            if i < len(options) - 1:
                description += "\n"

        embed = create_embed(
            title=question,
            description=description,
            color=discord.Color.blurple()
        )
        poll_message = await ctx.send(embed=embed)

        for i in range(len(options)):
            await poll_message.add_reaction(reactions[i])

        # Attendre la fin du sondage
        await asyncio.sleep(duration)

        # Récupérer le message mis à jour (avec les réactions)
        poll_message = await ctx.channel.fetch_message(poll_message.id)

        # Compter les votes
        results = {}
        for reaction in poll_message.reactions:
            if str(reaction.emoji) in reactions:
                # Compter seulement les utilisateurs qui ne sont pas des bots
                users = [user async for user in reaction.users() if not user.bot]
                results[reaction.emoji] = len(users)

        # Annoncer les résultats
        results_text = ""
        for emoji, count in results.items():
            option_index = reactions.index(emoji)
            results_text += f"{options[option_index]}: {count} votes\n"

        embed = create_embed(
            title=f"Résultats du sondage : {question}",
            description=results_text,
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Poll(bot))