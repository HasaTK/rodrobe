import discord 
import requests

from src                import config
from src.utils          import log
from src.utils.currency import isFloatOrDigit
from discord.ext        import commands 



class configs(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        log.success("Configs cog is ready")
    
    @commands.command(aliases=["s"])
    async def set(self,ctx, cfg, arg): 
        if str(cfg).lower() == "rates" or str(cfg).lower() == "rate":

            if not isFloatOrDigit(str(arg)):
                await ctx.reply("Argument for rates must be a number!")

            
            try:
                config.cfg_set("rates", arg)
                await ctx.reply(f"Successfully set rates to {arg}")
            except Exception as e:
                log.error(e,__name__)
                await ctx.reply(f"Error setting rate to {arg}")



async def setup(client):
    await client.add_cog(configs(client))
        
        