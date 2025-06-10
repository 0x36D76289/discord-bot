# DiscTeleBot

Bot Discord moderne avec architecture modulaire.

## 🏗️ Structure du projet

```
disctelebot/
├── .env                    # Variables d'environnement (tokens, etc.)
├── requirements.txt        # Dépendances Python
├── run.sh                 # Script de lancement
├── logs/                  # Dossier des logs (créé automatiquement)
└── src/                   # Code source
    ├── main.py           # Point d'entrée principal
    ├── bot.py            # Classe principale du bot
    ├── config.py         # Configuration centralisée
    ├── commands/         # Modules de commandes
    │   ├── __init__.py
    │   └── basic_commands.py
    └── utils/            # Utilitaires
        ├── __init__.py
        └── logger.py
```

## 🚀 Installation et lancement

1. **Installer les dépendances** :
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

2. **Configuration** :
   - Assurez-vous que votre fichier `.env` contient votre `DISCORD_TOKEN`
   - Le bot synchronisera automatiquement les commandes slash au démarrage

## 📝 Commandes disponibles

### Commandes de base
- `/ping` - Teste la latence du bot
- `/hello` - Salue l'utilisateur
- `/info` - Affiche des informations sur le bot
- `/serveur` - Affiche des informations sur le serveur

### Commandes utilitaires
- `/avatar [utilisateur]` - Affiche l'avatar d'un utilisateur
- `/roll [dés] [modificateur]` - Lance des dés (ex: 2d6)
- `/sondage <question> <options>` - Crée un sondage avec réactions
- `/remind <temps> [message]` - Programme un rappel

### Commandes d'administration (permissions requises)
- `/clear <nombre>` - Supprime des messages du canal
- `/kick <membre> [raison]` - Expulse un membre
- `/ban <membre> [raison] [jours]` - Bannit un membre
- `/timeout <membre> <durée> [raison]` - Met un membre en timeout

## 🔧 Ajouter de nouvelles commandes

1. Créez un nouveau fichier dans `src/commands/`
2. Créez une classe héritant de `commands.Cog`
3. Utilisez le décorateur `@app_commands.command()` pour les commandes slash
4. Ajoutez le cog dans `bot.py` avec `await self.add_cog(VotreCog(self))`

## 🔒 Permissions nécessaires

Le bot nécessite les permissions suivantes :
- `Send Messages`
- `Use Slash Commands`
- `Embed Links`
- `Read Message History`
