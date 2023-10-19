import discord 
import logging

from discord.ext    import commands 
from src            import config

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client 
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Help cog is ready")
    
    @commands.command(help="Gives a list of all commands")
    @commands.check(config.is_whitelisted)

    async def help(self, ctx):   
        description = ""

        for cmd  in self.client.walk_commands():
            description += f"`{cmd.name}` - {cmd.help}\n"
        
        embed = discord.Embed(
            title="Help",
            description=description
        )     
        
        await ctx.reply(embed=embed)


async def setup(client):
    await client.add_cog(Help(client))
        
        