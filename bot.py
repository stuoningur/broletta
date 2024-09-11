import logging
import logging.handlers
import os
import sys
from pathlib import Path

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


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)

stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(formatter)

file_handler = logging.handlers.TimedRotatingFileHandler(
    "loretta.log", when="midnight", backupCount=31, encoding="utf-8"
)
file_handler.setFormatter(formatter)


logger.addHandler(stdout_handler)
logger.addHandler(file_handler)


class Loretta(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["general"]["prefix"]),
            intents=intents,
            help_command=None,
        )
        self.logger = logger
        self.config = config

    async def load_cogs(self) -> None:
        cogs_dir = Path("cogs")
        for cog_file in cogs_dir.rglob("*.py"):
            cog_name = ".".join(cog_file.with_suffix("").parts)
            self.logger.info(f"Loaded cog: {cog_name}")
            await self.load_extension(f"{cog_name}")

    async def on_ready(self):
        if self.user:
            logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def setup_hook(self) -> None:
        await self.load_cogs()


load_dotenv()
bot_token = os.getenv("TOKEN")
if bot_token is None:
    sys.exit("Token not found in environment variables. Exiting...")
else:
    bot = Loretta()
    bot.run(bot_token, log_handler=None)
