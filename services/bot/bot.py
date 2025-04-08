import logging

import disnake
from disnake.ext import commands

from config import BOT_TOKEN
from logger_config import setup_log


setup_log()
log = logging.getLogger(__name__)

intents = disnake.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

bot.load_extension("bot.commands")
bot.reload_extension("bot.commands")



@bot.event
async def on_ready():
    log.info(f"BOT STARTED {bot.user.name}")

if __name__ == '__main__':
    bot.run(BOT_TOKEN)
