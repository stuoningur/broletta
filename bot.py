import sys
from pathlib import Path
import os

import discord
import tomllib
from discord.ext import commands
from dotenv import load_dotenv

config_file = (Path(__file__).parent).resolve() / "config.toml"

if config_file.exists():
    with open(config_file, "rb") as config_file_obj:
        config = tomllib.load(config_file_obj)
else:
    sys.exit("Configuration file 'config.toml' not found. Exiting...")

intents = discord.Intents.all()


class Loretta(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["general"]["prefix"]),
            intents=intents,
            help_command=None,
        )

    async def on_ready(self):
        if self.user:
            print(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

    async def on_error(self, event, *args, **kwargs):
        print(f"Error in {event}: {args[0]}")

    async def on_command_error(self, ctx, error):
        print(f"Error in command {ctx.command}: {error}")


load_dotenv()
bot_token = os.getenv("TOKEN")
if bot_token is None:
    sys.exit("Token not found in environment variables. Exiting...")
else:
    bot = Loretta()
    bot.run(bot_token)
