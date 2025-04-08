import disnake
from disnake.ext import commands
from disnake import Embed

import logging
from PlayerEngine import PlayerEngine
from TrackEngine import TrackEngine
from logger_config import setup_log

setup_log()
log = logging.getLogger(__name__)

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player_engine = PlayerEngine()
        self.track_engine = TrackEngine()
        
    @commands.slash_command(name="play", description="Play songs in voice chat")
    async def play(self, inter: disnake.ApplicationCommandInteraction, query: str):
        if not inter.author.voice.channel:
            await inter.response.send_message("You are not in a voice channel")
            return
        await inter.author.voice.channel.connect()
        queue = await self.player_engine.conntion(inter.author.voice.channel.id)
        await queue.add_in_queue()
        
        embed = Embed(
            title='Hello',
            description='World'
        )        
        embed.set_image(url='https://i.imgur.com/AfFp7pu.png')

        await inter.response.send_message(embed=embed)
        
def setup(bot):
    bot.add_cog(Player(bot))
    