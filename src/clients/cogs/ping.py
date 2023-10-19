import discord
import logging

from discord.ext    import commands
from src            import config

class ping(commands.Cog):

    def __init__(self, client):
        self.client = client 
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()

    async def on_ready(self):
        self.logger.info("Ping cog is ready")
    
    @commands.command(help="Testing command 🏓")
    @commands.check(config.is_whitelisted)

    async def ping(self, ctx):        
        await ctx.reply("Pong 🏓")


async def setup(client):
    await client.add_cog(ping(client))
        
        