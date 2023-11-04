import logging
import discord

from src import config
from src.utils import currency
from discord.ext import commands


class ConversionCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Conversion cog is ready")

    @commands.command(help="Converts robux to USD (using the rates config)", aliases=[
        "r2u", "robuxtocurrency", "r2c", "robux2usd"
    ])
    @commands.check(config.is_whitelisted)
    async def robuxtousd(self, ctx, robux_amount):
        print(currency.isFloatOrDigit(robux_amount))
        if not currency.isFloatOrDigit(robux_amount):
            await ctx.reply("robux_amount must be a number")
        else:
            rates = config.cfg_get("rates") or 3.5
            converted = currency.robux_price(robux=int(robux_amount), rate=rates)

            embed = discord.Embed(
                title="Robux -> USD",
                description=f"`{robux_amount}` robux is ~**${str(converted)}** (2DP) (using rates {str(rates)} / 1k)"
            )

            await ctx.reply(embed=embed)

    @commands.command(help="Converts USD to robux (using the rates config)", aliases=[
        "u2r", "currencytorobux", "c2r","usd2robux"
    ])
    @commands.check(config.is_whitelisted)
    async def usdtorobux(self, ctx, usd_amount):

        if not currency.isFloatOrDigit(usd_amount):
            await ctx.reply("usd_amount must be a number")
        else:
            rates = config.cfg_get("rates") or 3.5
            converted = currency.currency_to_robux(amount=int(usd_amount), rate=rates)

            embed = discord.Embed(
                title="USD -> Robux",
                description=f"`{usd_amount}` USD is ~ **{str(int(converted))}** robux (using rates {str(rates)} / 1k)"
            )

            await ctx.reply(embed=embed)


async def setup(client):
    await client.add_cog(ConversionCog(client))

