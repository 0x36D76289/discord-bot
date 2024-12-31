import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import create_embed

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    @commands.hybrid_command(name="aide", description="Affiche la liste des commandes ou l'aide pour une commande spécifique.")
    @app_commands.describe(command_name="Le nom de la commande pour laquelle vous voulez de l'aide (optionnel)")
    async def aide(self, ctx: commands.Context, command_name: str = None):
        """Affiche la liste des commandes ou l'aide pour une commande spécifique."""
        if command_name:
            command = self.bot.get_command(command_name)
            if command:
                embed = create_embed(
                    title=f"Aide pour la commande {command.name}",
                    description=command.help,
                    color=discord.Color.blue()
                )
                if command.signature:
                    embed.add_field(name="Utilisation", value=f"`/{command.name} {command.signature}`", inline=False)
                if command.aliases:
                    embed.add_field(name="Alias", value=", ".join(command.aliases), inline=False)
                await ctx.send(embed=embed)
            else:
                embed = create_embed(
                    title="Erreur",
                    description=f"Commande '{command_name}' non trouvée.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = create_embed(
                title="Liste des commandes",
                description="Voici la liste des commandes disponibles :",
                color=discord.Color.blue()
            )
            for cog_name, cog in self.bot.cogs.items():
                # Exclure les cogs sans commandes visibles (comme les listeners)
                visible_commands = [cmd for cmd in cog.get_commands() if not cmd.hidden]
                if visible_commands:
                    commands_list = ""
                    for command in visible_commands:
                        if isinstance(command, commands.HybridCommand):
                            commands_list += f"`/{command.name}`, "
                        else:
                            commands_list += f"`{command.name}`, "
                    if commands_list:
                        embed.add_field(name=cog_name, value=commands_list[:-2], inline=False)

            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))