"""
Commandes utilitaires avancées
"""
import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random
import asyncio

class PollView(discord.ui.View):
    """Vue interactive pour les sondages avec barres de progression"""
    
    def __init__(self, question: str, options: list, creator):
        super().__init__(timeout=300)  # 5 minutes de timeout
        self.question = question
        self.options = options
        self.creator = creator
        self.votes = {i: set() for i in range(len(options))}  # Dictionnaire des votes par option
        self.message = None
        
        # Créer les boutons pour chaque option
        for i, option in enumerate(options):
            button = PollButton(i, option, self)
            self.add_item(button)
        
        # Ajouter un bouton pour terminer le sondage
        if len(options) <= 4:  # Seulement si on a de la place
            self.add_item(EndPollButton(self))
    
    def create_poll_embed(self):
        """Crée l'embed du sondage avec les barres de progression"""
        total_votes = sum(len(voters) for voters in self.votes.values())
        
        embed = discord.Embed(
            title=self.question,
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.now()
        )
        
        # Ajouter les options avec barres de progression
        for i, option in enumerate(self.options):
            vote_count = len(self.votes[i])
            percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            
            # Créer la barre de progression
            filled_blocks = int(percentage / 10)  # 10 blocs max
            empty_blocks = 10 - filled_blocks
            
            progress_bar = "▓" * filled_blocks + "░" * empty_blocks
            
            # Emoji et couleur selon le pourcentage
            if percentage >= 50:
                emoji = "🟢"
            elif percentage >= 25:
                emoji = "🟡"
            else:
                emoji = "🔴"
            
            embed.add_field(
                name=f"{emoji} {option}",
                value=f"{progress_bar}\n**{vote_count} vote{'s' if vote_count != 1 else ''} • {percentage:.0f}%**",
                inline=False
            )
        
        # Footer avec informations
        embed.set_footer(
            text=f"{total_votes} vote{'s' if total_votes != 1 else ''} • Sondage créé par {self.creator.display_name}",
            icon_url=self.creator.display_avatar.url
        )
        
        return embed
    
    async def update_poll(self, interaction: discord.Interaction):
        """Met à jour l'affichage du sondage"""
        embed = self.create_poll_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        """Appelé quand la vue expire"""
        if self.message:
            # Désactiver tous les boutons
            for item in self.children:
                if hasattr(item, 'disabled'):
                    item.disabled = True
            
            embed = self.create_poll_embed()
            embed.color = discord.Color.red()
            embed.add_field(name="⏰ Sondage terminé", value="Ce sondage a expiré", inline=False)
            
            try:
                await self.message.edit(embed=embed, view=self)
            except discord.NotFound:
                pass

class PollButton(discord.ui.Button):
    """Bouton pour voter dans un sondage"""
    
    def __init__(self, option_index: int, option_text: str, poll_view):
        super().__init__(
            label=option_text[:80],  # Limiter la longueur du label
            style=discord.ButtonStyle.secondary,
            custom_id=f"poll_option_{option_index}"
        )
        self.option_index = option_index
        self.poll_view = poll_view
    
    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        
        # Vérifier si l'utilisateur a déjà voté
        current_vote = None
        for i, voters in self.poll_view.votes.items():
            if user_id in voters:
                current_vote = i
                break
        
        # Si l'utilisateur vote pour la même option, retirer son vote
        if current_vote == self.option_index:
            self.poll_view.votes[self.option_index].remove(user_id)
            await interaction.response.send_message("❌ Vote retiré !", ephemeral=True)
        else:
            # Retirer le vote précédent s'il existe
            if current_vote is not None:
                self.poll_view.votes[current_vote].remove(user_id)
            
            # Ajouter le nouveau vote
            self.poll_view.votes[self.option_index].add(user_id)
            await interaction.response.send_message("✅ Vote enregistré !", ephemeral=True)
        
        # Mettre à jour l'affichage
        embed = self.poll_view.create_poll_embed()
        await interaction.edit_original_response(embed=embed)

class EndPollButton(discord.ui.Button):
    """Bouton pour terminer un sondage"""
    
    def __init__(self, poll_view):
        super().__init__(
            label="Terminer le sondage",
            style=discord.ButtonStyle.danger,
            emoji="🔒"
        )
        self.poll_view = poll_view
    
    async def callback(self, interaction: discord.Interaction):
        # Seul le créateur peut terminer le sondage
        if interaction.user.id != self.poll_view.creator.id:
            await interaction.response.send_message("❌ Seul le créateur du sondage peut le terminer !", ephemeral=True)
            return
        
        # Désactiver tous les boutons
        for item in self.poll_view.children:
            if hasattr(item, 'disabled'):
                item.disabled = True
        
        # Créer l'embed final
        embed = self.poll_view.create_poll_embed()
        embed.color = discord.Color.green()
        embed.title = f"✅ {self.poll_view.question}"
        
        # Déterminer le gagnant
        total_votes = sum(len(voters) for voters in self.poll_view.votes.values())
        if total_votes > 0:
            winner_index = max(self.poll_view.votes.keys(), key=lambda k: len(self.poll_view.votes[k]))
            winner_votes = len(self.poll_view.votes[winner_index])
            winner_percentage = (winner_votes / total_votes * 100)
            
            embed.add_field(
                name="🏆 Résultat",
                value=f"**{self.poll_view.options[winner_index]}** remporte avec {winner_votes} vote{'s' if winner_votes != 1 else ''} ({winner_percentage:.0f}%)",
                inline=False
            )
        
        await interaction.response.edit_message(embed=embed, view=self.poll_view)

class UtilityCommands(commands.Cog):
    """Cog contenant des commandes utilitaires avancées"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="avatar", description="Affiche l'avatar d'un utilisateur")
    @app_commands.describe(user="L'utilisateur dont vous voulez voir l'avatar")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        """Affiche l'avatar d'un utilisateur"""
        target_user = user if user is not None else interaction.user
        
        embed = discord.Embed(
            title=f"Avatar de {target_user.display_name}",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        embed.set_image(url=target_user.display_avatar.url)
        embed.set_footer(text=f"Demandé par {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="roll", description="Lance un ou plusieurs dés")
    @app_commands.describe(
        dice="Format: NdX (ex: 2d6 pour 2 dés à 6 faces)",
        modifier="Modificateur à ajouter au résultat"
    )
    async def roll_dice(self, interaction: discord.Interaction, dice: str = "1d6", modifier: int = 0):
        """Lance des dés"""
        try:
            # Parser le format NdX
            if 'd' not in dice.lower():
                await interaction.response.send_message("Format invalide ! Utilisez NdX (ex: 2d6)", ephemeral=True)
                return
            
            parts = dice.lower().split('d')
            num_dice = int(parts[0]) if parts[0] else 1
            sides = int(parts[1])
            
            # Limites de sécurité
            if num_dice > 20:
                await interaction.response.send_message("Maximum 20 dés autorisés !", ephemeral=True)
                return
            if sides > 100:
                await interaction.response.send_message("Maximum 100 faces par dé !", ephemeral=True)
                return
            
            # Lancer les dés
            rolls = [random.randint(1, sides) for _ in range(num_dice)]
            total = sum(rolls) + modifier
            
            # Créer l'embed
            embed = discord.Embed(
                title="🎲 Lancer de dés",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now()
            )
            
            embed.add_field(name="Dés", value=f"{num_dice}d{sides}", inline=True)
            embed.add_field(name="Résultats", value=" + ".join(map(str, rolls)), inline=True)
            embed.add_field(name="Modificateur", value=f"+{modifier}" if modifier >= 0 else str(modifier), inline=True)
            embed.add_field(name="Total", value=f"**{total}**", inline=False)
            
            await interaction.response.send_message(embed=embed)
            
        except ValueError:
            await interaction.response.send_message("Format invalide ! Utilisez NdX (ex: 2d6)", ephemeral=True)
    
    @app_commands.command(name="sondage", description="Crée un sondage interactif avec barres de progression")
    @app_commands.describe(
        question="La question du sondage",
        options="Les options séparées par des virgules (max 6)"
    )
    async def poll(self, interaction: discord.Interaction, question: str, options: str):
        """Crée un sondage avec interface interactive"""
        option_list = [opt.strip() for opt in options.split(',') if opt.strip()]
        
        if len(option_list) < 2:
            await interaction.response.send_message("Il faut au moins 2 options !", ephemeral=True)
            return
        
        if len(option_list) > 6:
            await interaction.response.send_message("Maximum 6 options autorisées pour une meilleure lisibilité !", ephemeral=True)
            return
        
        # Créer la vue interactive
        poll_view = PollView(question, option_list, interaction.user)
        
        # Créer l'embed initial
        embed = poll_view.create_poll_embed()
        
        # Envoyer le message avec la vue
        await interaction.response.send_message(embed=embed, view=poll_view)
        
        # Stocker le message pour les mises à jour
        poll_view.message = await interaction.original_response()
    
    @app_commands.command(name="sondage_simple", description="Crée un sondage oui/non/neutre rapide")
    @app_commands.describe(question="La question du sondage")
    async def simple_poll(self, interaction: discord.Interaction, question: str):
        """Crée un sondage simple oui/non/neutre"""
        # Options par défaut
        options = ["oui", "non", "neutre"]
        
        # Créer la vue interactive
        poll_view = PollView(question, options, interaction.user)
        
        # Créer l'embed initial
        embed = poll_view.create_poll_embed()
        
        # Envoyer le message avec la vue
        await interaction.response.send_message(embed=embed, view=poll_view)
        
        # Stocker le message pour les mises à jour
        poll_view.message = await interaction.original_response()
    
    @app_commands.command(name="remind", description="Programme un rappel")
    @app_commands.describe(
        time="Temps en minutes",
        message="Message du rappel"
    )
    async def remind(self, interaction: discord.Interaction, time: int, message: str = "Rappel !"):
        """Programme un rappel"""
        if time <= 0 or time > 1440:  # Max 24h
            await interaction.response.send_message("Le temps doit être entre 1 et 1440 minutes (24h) !", ephemeral=True)
            return
        
        await interaction.response.send_message(f"⏰ Rappel programmé dans {time} minute(s) !")
        
        # Attendre
        await asyncio.sleep(time * 60)
        
        # Envoyer le rappel
        embed = discord.Embed(
            title="⏰ Rappel",
            description=message,
            color=discord.Color.orange(),
            timestamp=datetime.datetime.now()
        )
        
        embed.set_footer(text=f"Rappel pour {interaction.user.display_name}")
        
        try:
            await interaction.user.send(embed=embed)
        except discord.Forbidden:
            # Si on ne peut pas envoyer en MP, envoyer dans le canal
            await interaction.followup.send(f"{interaction.user.mention} {message}", embed=embed)

async def setup(bot):
    """Fonction pour charger le cog"""
    await bot.add_cog(UtilityCommands(bot))
