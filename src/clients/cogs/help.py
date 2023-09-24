import discord 
import requests
from src.utils      import log
from discord.ext    import commands 

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client 
    @commands.Cog.listener()
    async def on_ready(self):
        log.success("Help cog is ready")
    
    @commands.command(help="Gives a list of all commands")
    async def help(self, ctx):   
        description = ""

        for cmd  in self.client.walk_commands():
            description += f"`{cmd.name}` - {cmd.help}\n"
        
        embed = discord.Embed(
            title="Help",
            color=0x1d201f,
            description=description
        )     
        
        await ctx.reply(embed=embed)


async def setup(client):
    await client.add_cog(Help(client))
        
        