import disnake
from disnake.ext import commands
import os
from src.execve import execute_code
import random

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


def is_not_authorized(user):
    # if user.id == 202004386958934017 or user.bot:
    #     return True
    return False


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


class ExecveButton(disnake.ui.View):
    def __init__(self, language, code, author_id):
        super().__init__()
        self.language = language
        self.code = code
        self.author_id = author_id

    @disnake.ui.button(label="Relance pitier", style=disnake.ButtonStyle.green)
    async def execve_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("ratio.", ephemeral=True)
            return

        stdout, stderr = execute_code(self.language, self.code)
        if stderr:
            result = f"**Error**:\n```log\n{stderr}```"
        else:
            result = f"**Result**:\n```{stdout}```"
        await interaction.response.send_message(result)


@bot.command()
async def execve(ctx, *, arg):
    if is_not_authorized(ctx.author):
        await ctx.send("You are not authorized to use this bot.")
        return

    def parse_code_block(code_block):
        try:
            header, *code = code_block.split('\n', 2)
            language = header.split('```')[1].strip()
            code = '\n'.join(code).rstrip('```').strip()
            return language, code
        except Exception as e:
            return None, None

    language, code = parse_code_block(arg)
    if not language or not code:
        await ctx.send("Invalid code block format.")
        return

    stdout, stderr = execute_code(language, code)
    if stderr:
        result = f"**Error**:\n```log\n{stderr}```"
    else:
        result = f"**Result**:\n```{stdout}```"

    view = ExecveButton(language, code, ctx.author.id)
    await ctx.send(result, view=view)


@bot.command()
async def wallpaper(ctx):
    if is_not_authorized(ctx.author):
        await ctx.send("You are not authorized to use this bot.")
        return

    await ctx.send(f"https://source.unsplash.com/random/1920x1080?nature,water,{random.randint(0, 100)}")


@bot.command()
async def clear(ctx, arg):
    if is_not_authorized(ctx.author):
        await ctx.send("You are not authorized to use this bot.")
        return

    if arg == "all":
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=int(arg))

bot.run(DISCORD_TOKEN)
