# Discord Bot

This is a Dockerized Discord bot built with Python. It includes basic moderation commands and a general **!ping** command.

## Prerequisites

-   Docker
-   Docker Compose
-   A Discord Bot Token

## Getting Started

1. **Clone the repository:**

```sh
git clone [repository-url]
cd discord-bot
```

2. **Set up the environment variables:**

Create a **.env** file in the root directory of the project based on the **.env.example** file and fill in your Discord bot token:

```sh
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

3. **Build and run the Docker container:**

```sh
docker-compose up --build
```

This command builds the Docker image and starts the container. The bot should now be running and connected to your Discord server.

## Development

### Adding New Commands

To add new commands, create a new Python file within the appropriate category directory under **src/commands/**. Each command should be a class that inherits from **BaseCommand**.

#### Example: Adding a new command category and command

1. Create a new directory **src/commands/utility/**.
2. Create **src/commands/utility/\_\_init\_\_.py**.
3. Create **src/commands/utility/echo.py**:

```python
from discord.ext import commands
from src.base_command import BaseCommand

class EchoCommand(BaseCommand):
	def __init__(self, bot):
		super().__init__(bot)

	@commands.command(name="echo")
	async def echo(self, ctx, *, message: str):
		"""Repeats the message."""
		await ctx.send(message)
```

4. Update **src/main.py** to load the new command:

```python
# ... other imports
from src.commands.utility.echo import EchoCommand

# ...

async def setup_hook():
	# ... other cogs
	await bot.add_cog(EchoCommand(bot))
bot.setup_hook = setup_hook

# ...
```

### Running Tests

To run tests and ensure that your commands are working correctly, you can use the provided test suite. Make sure you have pytest installed:

**pip install pytest**

Then, run the tests with:

**pytest src/tests**

## Extending the Bot

You can extend the bot by adding more command categories and commands. Ensure each command category is a subdirectory under **src/commands/** and each command is a class inheriting from **BaseCommand**.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.