import random
import discord
import logging
import asyncio

from src.utils import assets
from src.utils import groups
from src.exceptions import (
    InvalidAssetId,
    InvalidAssetType,
    AssetDetailsNotFound,
    InvalidGroupID,
    InsufficientFundsException,
    AccountTerminatedException
)

from src.clients import accounts
from discord.ext import commands
from src import config


class Republish(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)
        self.uploader = accounts.RobloxAccount(config.cfg_file["group"]["uploader_cookie"])

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Republishing cog is ready")

    @commands.command(help="uploads the asset to your own group", aliases=["republish", "repub", "rp", "rb"])
    @commands.check(config.is_whitelisted)
    async def steal(self, ctx, asset_id, remove_watermark=True):
        try:
            embed = discord.Embed(
                title=f"Attempting to republish asset ",
                color=config.EmbedColors.INFO
            )

            message = await ctx.reply(embed=embed)
            repubAsset = assets.republish_asset(asset_id=asset_id, remove_watermark=remove_watermark,
                                                uploader=self.uploader)
            if repubAsset:
                pub_id = repubAsset["response"]["assetId"]

                embed.title = "Republished asset successfully"
                embed.color = config.EmbedColors.SUCCESS
                embed.description = f"The republished asset can be found [here](https://www.roblox.com/catalog/{pub_id})"

                await message.edit(embed=embed)

        except InsufficientFundsException:
            embed.title = "Insufficient Funds"
            embed.color = config.EmbedColors.ERROR
            embed.description = "The uploader account does not have enough robux to publish this asset"

            await message.edit(embed=embed)

        except InvalidAssetId:

            embed.title = "Invalid Asset Id"
            embed.color = config.EmbedColors.ERROR
            embed.description = "The asset id provided is invalid"

            await message.edit(embed=embed)

        except AssetDetailsNotFound:

            self.logger.error("Asset details were not found")
            embed.title = "Error"
            embed.color = config.EmbedColors.ERROR
            embed.description = "Error while attempting to attempting to get asset details."

            await message.edit(embed=embed)
        except InvalidAssetType:
            embed.title = "Invalid Asset Type"
            embed.color = config.EmbedColors.ERROR
            embed.description = "The asset type provided is invalid"

            await message.edit(embed=embed)

        except Exception as e:

            self.logger.error(e)

            embed.title = "Error"
            embed.description = f'```{e}```'
            embed.color = config.EmbedColors.ERROR

            await message.edit(embed=embed)

    @commands.command(help="republishes all the assets an existing group has to your group",
                      aliases=["sg", "stealgroup", "rg", "republishgroup", "repgroup", "repg"])
    @commands.check(config.is_whitelisted)
    async def sgroup(self, ctx, group_id, remove_watermark=True):

        try:
            group_info = groups.getGroupInfo(group_id=group_id)
        except InvalidGroupID:
            embed = discord.Embed(
                title="Invalid group ID",
                description="The group id provided is invalid",
                color=config.EmbedColors.ERROR
            )

            await ctx.reply(embed=embed)

        embed = discord.Embed(
            title="Attempting to upload assets",
            color=config.EmbedColors.INFO
        )

        message = await ctx.reply(embed=embed)

        upload_count = 0
        np_cursor = None
        # TODO: recode this
        while True:
            cached_assets = self.uploader.getGroupAssets(group_id=group_id,
                                                         cursor=np_cursor)
            grequest = cached_assets["obj"]

            np_cursor = grequest.json()["nextPageCursor"]
            if cached_assets["data"]:
                if grequest.ok:

                    for asset in cached_assets["data"]:
                        asset_id = asset["id"]

                        if config.cfg_file["assets"]["ignore_duplicates"] and config.is_cached(asset_id=asset_id):
                            self.logger.info(f"Skipping asset '{asset_id}' - already cached")
                            pass
                        else:
                            try:

                                upload = assets.republish_asset(
                                    asset_id=asset["id"],
                                    remove_watermark=remove_watermark,
                                    uploader=self.uploader
                                )

                                if upload:

                                    if config.cfg_file["assets"]["ignore_duplicates"]:
                                        config.add_cache(asset_id=asset_id)

                                    pub_id = upload["response"]["assetId"]
                                    pub_name = upload["response"]["displayName"]

                                    upload_count += 1

                                    self.logger.info(f"Uploaded asset  '{pub_name}' with id: {pub_id}")

                                    embed.title = "Last asset published"
                                    embed.description = f"Last published [{pub_name}](https:/www.roblox.com/catalog/{pub_id})"
                                    embed.color = config.EmbedColors.INFO

                                    await message.edit(embed=embed)
                                else:
                                    self.logger.error(upload)

                            except AccountTerminatedException:
                                embed.title = "Account Terminated"
                                embed.color = config.EmbedColors.ERROR
                                embed.description = f"A total of {upload_count} assets were uploaded before being terminated."
                                await (message.edit(embed=embed))
                                return

                            except InsufficientFundsException:

                                embed.title = "Robux Finished"
                                embed.color = config.EmbedColors.ERROR
                                embed.description = f"A total of {upload_count} assets were uploaded before being running out of robux."
                                await message.edit(embed=embed)
                                return

                            except Exception as e:
                                embed.title = "Error"
                                embed.description = f'```{e}```'
                                embed.color = config.EmbedColors.ERROR

                                await ctx.reply(embed=embed)
                                return

    @commands.command(help="Scrapes assets from the front page and reuploads them",
                      aliases=["fpscrape", "find", "getpop", "getpopulars"])
    @commands.check(config.is_whitelisted)
    async def scrape(self, ctx, scrape_count, keyword=None):

        if not scrape_count.isnumeric():
            embed = discord.Embed(
                title="Error",
                color=config.EmbedColors.ERROR,
                description="`scrape_count` must be an integer"
            )
            await ctx.reply(embed=embed)
            return

        embed = discord.Embed(
            title="Attempting to scrape and reupload assets..",
            color=config.EmbedColors.INFO
        )

        message = await ctx.reply(embed=embed)

        scrape_count = int(scrape_count)
        upload_count = 0
        np_cursors = {"s": None, "p": None}

        while True:

            scraped_shirts = assets.get_fp_assets(subcategory="ClassicShirts", limit=120,
                                                  keyword=keyword, cursor=np_cursors["s"])
            scraped_pants = assets.get_fp_assets(subcategory="ClassicPants", limit=120,
                                                 keyword=keyword, cursor=np_cursors["p"])

            scraped_assets = scraped_pants["data"] + scraped_shirts["data"]
            random.shuffle(scraped_assets)

            for asset in scraped_assets:

                if upload_count >= scrape_count:
                    embed.title = "Success"
                    embed.description = f"Successfully uploaded `{upload_count}` assets."
                    embed.color = config.EmbedColors.SUCCESS

                    await ctx.reply(embed=embed)
                    return

                asset_id = asset["id"]
                if config.cfg_file["assets"]["ignore_duplicates"] and config.is_cached(asset_id=asset_id):
                    self.logger.info(f"Skipping asset '{asset_id}' - already cached")
                    pass

                else:
                    try:

                        upload = assets.republish_asset(
                            asset_id=asset_id,
                            remove_watermark=True,
                            uploader=self.uploader
                        )
                        self.logger.debug(upload)

                        if upload:
                            if config.cfg_file["assets"]["ignore_duplicates"]:
                                config.add_cache(asset_id=asset_id)

                            pub_id = upload["response"]["assetId"]
                            pub_name = upload["response"]["displayName"]
                            upload_count += 1

                            self.logger.info(f"Uploaded asset  of '{str(pub_name)}' with id: {pub_id}")

                            embed.title = "Last asset published"
                            embed.color = config.EmbedColors.INFO
                            embed.description = f"Last asset published was [{pub_name}](https://www.roblox.com/catalog/{pub_id})"
                            await message.edit(embed=embed)
                        else:
                            self.logger.error(upload)

                    except AccountTerminatedException:
                        embed.title = "Account Terminated"
                        embed.color = config.EmbedColors.ERROR
                        embed.description = f"A total of {upload_count} assets were uploaded before being terminated."
                        await message.edit(embed=embed)
                        return

                    except InsufficientFundsException:

                        embed.title = "Robux Finished"
                        embed.color = config.EmbedColors.ERROR
                        embed.description = f"A total of {upload_count} assets were uploaded before being running out of robux."
                        await message.edit(embed=embed)
                        return

                    except Exception as e:
                        embed.title = "Error"
                        embed.description = f'```{e}```'
                        embed.color = config.EmbedColors.ERROR

                        await ctx.reply(embed=embed)
                        return

            np_cursors["s"] = {scraped_shirts["nextPageCursor"]}
            np_cursors["p"] = {scraped_pants["nextPageCursor"]}


async def setup(client):
    await client.add_cog(Republish(client))
