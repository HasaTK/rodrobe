import discord
import logging

from discord.ext import commands
from src import config
from src.clients import accounts


class AccountCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)
        self.uploader = accounts.RobloxAccount(config.cfg_file["group"]["uploader_cookie"])
        self.holder   = accounts.RobloxAccount(config.cfg_file["group"]["holder_cookie"])
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Accounts cog is ready")

    @commands.command(help="Shows the accounts connected along with the robux they have")
    @commands.check(config.is_whitelisted)
    async def accounts(self, ctx):
        try:
            embed = discord.Embed(
                title="Accounts",
                color=config.EmbedColors.INFO,
            )
            embed.add_field(
                name="Uploader",
                value=f"Name: [{self.uploader.name}](https://www.roblox.com/users/{self.uploader.user_id})\nRobux: {self.uploader.getRobux()}",
                inline=False
            )
            embed.add_field(
                name="Holder",
                value=f"Name: [{self.holder.name}](https://www.roblox.com/users/{self.holder.user_id})\nRobux: {self.holder.getRobux()}"
            )

            await ctx.reply(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Error",
                color=config.EmbedColors.ERROR,
                description=f"```{e}```"
            )

            await ctx.reply(embed=embed)


async def setup(client):
    await client.add_cog(AccountCog(client))

