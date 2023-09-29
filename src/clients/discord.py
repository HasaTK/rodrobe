import os 
import discord, asyncio

from src            import config
from src.utils      import log
from discord.ext    import commands 

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(
    intents=intents,
    command_prefix=config.get("discord_bot_prefix"),
    help_command=None
)

async def loadCogs():
    """
    Loads all the cogs in the cog directory 
    """

    for file in os.listdir("src/clients/cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"src.clients.cogs.{file[:-3]}")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
       
        embed = discord.Embed(
            title = "Missing arguments",
            color = config.EmbedColors.ERROR,
            description = f"**Correct Usage:** `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`"
        )

        await ctx.reply(embed=embed)


async def main():
    log.info("Starting discord bot")
    await loadCogs()
    await client.start(config.get("discord_bot_token"))


