"""
Commandes d'administration
"""
import discord
from discord import app_commands
from discord.ext import commands
import datetime

class AdminCommands(commands.Cog):
    """Cog contenant les commandes d'administration"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="clear", description="Supprime des messages du canal")
    @app_commands.describe(amount="Nombre de messages à supprimer (max 100)")
    @app_commands.default_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        """Supprime des messages du canal"""
        if amount <= 0 or amount > 100:
            await interaction.response.send_message("Le nombre doit être entre 1 et 100 !", ephemeral=True)
            return
        
        # Vérifier les permissions
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Vous n'avez pas la permission de gérer les messages !", ephemeral=True)
            return
        
        try:
            deleted = await interaction.channel.purge(limit=amount)
            
            embed = discord.Embed(
                title="🗑️ Messages supprimés",
                description=f"**{len(deleted)}** message(s) supprimé(s) avec succès !",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now()
            )
            
            embed.set_footer(text=f"Par {interaction.user.display_name}")
            
            # Répondre avec un message éphémère
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message("Je n'ai pas les permissions pour supprimer des messages !", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erreur lors de la suppression : {e}", ephemeral=True)
    
    @app_commands.command(name="kick", description="Expulse un membre du serveur")
    @app_commands.describe(
        member="Le membre à expulser",
        reason="Raison de l'expulsion"
    )
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison spécifiée"):
        """Expulse un membre du serveur"""
        # Vérifications de sécurité
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("Vous n'avez pas la permission d'expulser des membres !", ephemeral=True)
            return
        
        if member == interaction.user:
            await interaction.response.send_message("Vous ne pouvez pas vous expulser vous-même !", ephemeral=True)
            return
        
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("Vous ne pouvez pas expulser ce membre (rôle supérieur ou égal) !", ephemeral=True)
            return
        
        try:
            # Envoyer un message privé au membre avant l'expulsion
            try:
                dm_embed = discord.Embed(
                    title="🚪 Expulsion",
                    description=f"Vous avez été expulsé du serveur **{interaction.guild.name}**",
                    color=discord.Color.orange()
                )
                dm_embed.add_field(name="Raison", value=reason, inline=False)
                dm_embed.add_field(name="Modérateur", value=interaction.user.display_name, inline=False)
                
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                pass  # Si on ne peut pas envoyer de MP
            
            # Expulser le membre
            await member.kick(reason=f"Par {interaction.user} : {reason}")
            
            # Confirmer l'action
            embed = discord.Embed(
                title="🚪 Membre expulsé",
                color=discord.Color.orange(),
                timestamp=datetime.datetime.now()
            )
            
            embed.add_field(name="Membre", value=f"{member} ({member.id})", inline=False)
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message("Je n'ai pas les permissions pour expulser ce membre !", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erreur lors de l'expulsion : {e}", ephemeral=True)
    
    @app_commands.command(name="ban", description="Bannit un membre du serveur")
    @app_commands.describe(
        member="Le membre à bannir",
        reason="Raison du bannissement",
        delete_days="Nombre de jours de messages à supprimer (0-7)"
    )
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison spécifiée", delete_days: int = 0):
        """Bannit un membre du serveur"""
        # Vérifications de sécurité
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("Vous n'avez pas la permission de bannir des membres !", ephemeral=True)
            return
        
        if member == interaction.user:
            await interaction.response.send_message("Vous ne pouvez pas vous bannir vous-même !", ephemeral=True)
            return
        
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("Vous ne pouvez pas bannir ce membre (rôle supérieur ou égal) !", ephemeral=True)
            return
        
        if delete_days < 0 or delete_days > 7:
            await interaction.response.send_message("Le nombre de jours doit être entre 0 et 7 !", ephemeral=True)
            return
        
        try:
            # Envoyer un message privé au membre avant le bannissement
            try:
                dm_embed = discord.Embed(
                    title="🔨 Bannissement",
                    description=f"Vous avez été banni du serveur **{interaction.guild.name}**",
                    color=discord.Color.red()
                )
                dm_embed.add_field(name="Raison", value=reason, inline=False)
                dm_embed.add_field(name="Modérateur", value=interaction.user.display_name, inline=False)
                
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                pass  # Si on ne peut pas envoyer de MP
            
            # Bannir le membre
            await member.ban(reason=f"Par {interaction.user} : {reason}", delete_message_days=delete_days)
            
            # Confirmer l'action
            embed = discord.Embed(
                title="🔨 Membre banni",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now()
            )
            
            embed.add_field(name="Membre", value=f"{member} ({member.id})", inline=False)
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Messages supprimés", value=f"{delete_days} jour(s)", inline=True)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message("Je n'ai pas les permissions pour bannir ce membre !", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erreur lors du bannissement : {e}", ephemeral=True)
    
    @app_commands.command(name="timeout", description="Met un membre en timeout")
    @app_commands.describe(
        member="Le membre à mettre en timeout",
        duration="Durée en minutes (max 40320 = 28 jours)",
        reason="Raison du timeout"
    )
    @app_commands.default_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "Aucune raison spécifiée"):
        """Met un membre en timeout"""
        # Vérifications
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("Vous n'avez pas la permission de modérer les membres !", ephemeral=True)
            return
        
        if member == interaction.user:
            await interaction.response.send_message("Vous ne pouvez pas vous mettre en timeout vous-même !", ephemeral=True)
            return
        
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("Vous ne pouvez pas mettre ce membre en timeout (rôle supérieur ou égal) !", ephemeral=True)
            return
        
        if duration <= 0 or duration > 40320:  # Max 28 jours
            await interaction.response.send_message("La durée doit être entre 1 et 40320 minutes (28 jours) !", ephemeral=True)
            return
        
        try:
            # Calculer la durée
            timeout_until = datetime.datetime.now() + datetime.timedelta(minutes=duration)
            
            # Appliquer le timeout
            await member.timeout(timeout_until, reason=f"Par {interaction.user} : {reason}")
            
            # Confirmer l'action
            embed = discord.Embed(
                title="⏱️ Membre en timeout",
                color=discord.Color.orange(),
                timestamp=datetime.datetime.now()
            )
            
            embed.add_field(name="Membre", value=f"{member} ({member.id})", inline=False)
            embed.add_field(name="Durée", value=f"{duration} minute(s)", inline=True)
            embed.add_field(name="Fin", value=f"<t:{int(timeout_until.timestamp())}:R>", inline=True)
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Modérateur", value=interaction.user.mention, inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message("Je n'ai pas les permissions pour mettre ce membre en timeout !", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erreur lors du timeout : {e}", ephemeral=True)

async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(AdminCommands(bot))
