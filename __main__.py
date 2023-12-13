import disnake
import os
from execve import execute_code

intents = disnake.Intents.default()
intents.message_content = True
client = disnake.Client(intents=intents)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


def is_authorized(user):
    return True


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


def parse_code_block(code_block):
    try:
        header, *code = code_block.split('\n', 2)
        language = header.split('```')[1].strip()
        code = '\n'.join(code).rstrip('```').strip()
        return language, code
    except Exception as e:
        return None, None


async def handle_execve_command(message, args):
    if not args:
        await message.channel.send("No code provided.")
        return

    code_block = args[0]
    if not code_block.startswith('```') or not code_block.endswith('```'):
        await message.channel.send("Please use code blocks to send code.")
        return

    # Extract language and code from the code block
    language, code = parse_code_block(code_block)
    if not language or not code:
        await message.channel.send("Invalid code block format.")
        return

    # Execute code in Docker and get the result
    stdout, stderr = execute_code(language, code)
    if stderr:
        result = f"**Error**:\n```log\n{stderr}```"
    else:
        result = f"**Result**:\n```{stdout}```"
    await message.channel.send(result)


@client.event
async def on_message(message):
    if message.author == client.user or not is_authorized(message.author):
        return

    if message.content.startswith('$'):
        command, *args = message.content[1:].split(maxsplit=1)
        if command == 'execve':
            await handle_execve_command(message, args)
        elif command == "ping":
            await message.channel.send("pong")


client.run(DISCORD_TOKEN)
