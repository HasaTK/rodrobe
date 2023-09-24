import discord 
import requests

from src.utils      import log
from discord.ext    import commands 
from src            import config

class ping(commands.Cog):

    def __init__(self, client):
        self.client = client 
        
    @commands.Cog.listener()

    async def on_ready(self):
        log.success("Ping cog is ready")
    
    @commands.command(help="Testing command 🏓")
    @commands.check(config.is_whitelisted)

    async def ping(self, ctx):        
        await ctx.reply("Pong 🏓")


async def setup(client):
    await client.add_cog(ping(client))
        
        