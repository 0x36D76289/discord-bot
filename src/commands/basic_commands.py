"""
Commandes de base du bot
"""
import discord
from discord import app_commands
from discord.ext import commands
import random
import datetime

class BasicCommands(commands.Cog):
    """Cog contenant les commandes de base"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Teste la latence du bot")
    async def ping(self, interaction: discord.Interaction):
        """Commande ping pour tester la latence"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latence: **{latency}ms**",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="hello", description="Salue l'utilisateur")
    async def hello(self, interaction: discord.Interaction):
        """Commande pour saluer l'utilisateur"""
        user = interaction.user
        
        salutations = [
            f"Salut {user.mention} ! 👋",
            f"Bonjour {user.display_name} ! 😊",
            f"Coucou {user.mention} ! ✨",
            f"Hey {user.display_name} ! 🎉"
        ]
        
        salutation = random.choice(salutations)
        
        embed = discord.Embed(
            description=salutation,
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="info", description="Affiche des informations sur le bot")
    async def info(self, interaction: discord.Interaction):
        """Affiche des informations sur le bot"""
        bot_user = self.bot.user
        guild_count = len(self.bot.guilds)
        
        embed = discord.Embed(
            title="📋 Informations du Bot",
            color=discord.Color.purple(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(name="Nom", value=bot_user.display_name, inline=True)
        embed.add_field(name="ID", value=bot_user.id, inline=True)
        embed.add_field(name="Serveurs", value=guild_count, inline=True)
        embed.add_field(name="Latence", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        embed.set_thumbnail(url=bot_user.avatar.url if bot_user.avatar else None)
        embed.set_footer(text="Bot Discord", icon_url=bot_user.avatar.url if bot_user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="serveur", description="Affiche des informations sur le serveur")
    async def server_info(self, interaction: discord.Interaction):
        """Affiche des informations sur le serveur"""
        guild = interaction.guild
        
        if not guild:
            await interaction.response.send_message("Cette commande ne peut être utilisée qu'dans un serveur!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=f"📊 Informations sur {guild.name}",
            color=discord.Color.gold(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(name="Propriétaire", value=guild.owner.mention if guild.owner else "Inconnu", inline=True)
        embed.add_field(name="Membres", value=guild.member_count, inline=True)
        embed.add_field(name="Créé le", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Région", value=str(guild.preferred_locale), inline=True)
        embed.add_field(name="Niveau de vérification", value=str(guild.verification_level), inline=True)
        embed.add_field(name="Salons", value=len(guild.channels), inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(BasicCommands(bot))
