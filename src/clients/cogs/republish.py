import discord 
import logging

from src.utils      import assets
from src.utils      import groups
from src.exceptions import (
    InvalidAssetId,
    InvalidAssetType,
    AssetDetailsNotFound,
    InvalidGroupID,
    AccountTerminatedException
)

from src.clients    import accounts
from discord.ext    import commands 
from src            import config


class Republish(commands.Cog):

    def __init__(self, client):
        self.client = client 
        self.logger = logging.getLogger(__name__)
        self.uploader = accounts.RobloxAccount(config.cfg_file["group"]["uploader_cookie"])

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Republishing cog is ready")
    
    @commands.command(help="uploads the asset to your own group", aliases = ["republish", "repub", "rp", "rb"])
    @commands.check(config.is_whitelisted)
    async def steal(self, ctx, asset_id, remove_watermark = True):
        try:
            embed = discord.Embed(
                title=f"Attempting to republish asset ",
                color=config.EmbedColors.INFO
            )

            message = await ctx.reply(embed=embed)
            repubAsset = assets.republish_asset(asset_id=asset_id,remove_watermark=remove_watermark,uploader=self.uploader)
            if repubAsset:

                pub_id = repubAsset["response"]["assetId"] 
            
                embed.title = "Republished asset successfully"
                embed.color = config.EmbedColors.SUCCESS
                embed.description = f"The republished asset can be found [here](https://www.roblox.com/catalog/{pub_id})"
                

                await message.edit(embed = embed)

        except InvalidAssetId:
            
            embed.title = "Invalid Asset Id"
            embed.color = config.EmbedColors.ERROR
            embed.description = "The asset id provided is invalid"

            await message.edit(embed = embed)
        
        except AssetDetailsNotFound:

            self.logger.error("Asset details were not found")
            embed.title = "Error"
            embed.color = config.EmbedColors.ERROR
            embed.description = "Error while attempting to attempting to get asset details."
            

            await message.edit(embed=embed)
        except InvalidAssetType:
            embed.title="Invalid Asset Type"
            embed.color=config.EmbedColors.ERROR
            embed.description="The asset type provided is invalid"
            

            await message.edit(embed=embed)
         
        except Exception as e:
            
            self.logger.error(e)

            embed.title = "Error"
            embed.description=f'```{e}```'
            embed.color= config.EmbedColors.ERROR
        

            await message.edit(embed=embed)
    
    @commands.command(help="republishes all the assets an existing group has to your group", aliases = ["sg", "stealgroup", "rg", "republishgroup","repgroup","repg"])
    @commands.check(config.is_whitelisted)

    async def sgroup(self, ctx, group_id, remove_watermark = True):
        
        try: 
            group_info = groups.getGroupInfo(group_id=group_id)
        except InvalidGroupID:
            embed = discord.Embed(
                title="Invalid group ID",
                description="The group id provided is invalid",
                color=config.EmbedColors.ERROR
            )

            await ctx.reply(embed = embed)

        uploader = accounts.RobloxAccount(config.cfg_file["group"]["uploader_cookie"])
        cached_assets = uploader.getGroupAssets(group_id=group_id)
    
        embed = discord.Embed(
            title = "Attempting to upload assets",
            color = config.EmbedColors.INFO
        )

        message = await ctx.reply(embed=embed)

        upload_count = 0
        while True:
            try:
                if cached_assets["data"]:
                    request = cached_assets["obj"]
                    if request.ok:
                        for asset in cached_assets["data"]:
                            upload = assets.republish_asset(
                                asset_id=asset["id"],
                                remove_watermark=remove_watermark,
                                uploader=self.uploader
                            )
                            if upload:
                                upload_count += 1

                                pub_id = upload["response"]["assetId"] 
                                pub_name = upload["response"]["displayName"]
                                self.logger.info(f"Uploaded asset  '{pub_name}' with id: {pub_id}")
                                
                                embed.title="Last asset published",
                                embed.description=f"Last published [{pub_name}](https:/www.roblox.com/catalog/{pub_id})",
                                embed.color=config.EmbedColors.INFO

                                await message.edit(embed=embed)
                            else:
                                self.logger.error(upload)
                    
                    else:
                        if "Failed to pay the associated fees" in str(request.text) or "InsufficientFunds" in str(request.text):
                            embed.title ="Report"
                            embed.color=config.EmbedColors.ERROR
                            embed.description=f"A total of {upload_count} assets were uploaded before running out of robux."
                            
                            await ctx.reply(embed=embed)

                        elif "user is moderated" in str(request.text).lower():
                            embed.title="Report"
                            embed.color=config.EmbedColors.ERROR
                            embed.description=f"A total of {upload_count} assets were uploaded before being terminated."

                            await ctx.reply(embed=embed)

                        else:
                            embed.title = "Report"
                            embed.color=config.EmbedColors.ERROR
                            embed.description=f"A total of {upload_count} assets were before encountering an error.\nError:\n```{request.text}```"

                            await ctx.reply(embed=embed)

                    cached_assets = uploader.getGroupAssets(group_id=group_id, cursor=cached_assets["obj"]["nextPageCursor"])
                else:
                    break

            except AccountTerminatedException:
                embed.title="Account Terminated"
                embed.color=config.EmbedColors.ERROR
                embed.description=f"A total of {upload_count} assets were uploaded before being terminated."

                await ctx.reply(embed=embed)

            except Exception as e:
                embed.title="Error"
                embed.description=f'```{e}```'
                embed.color=config.EmbedColors.ERROR
        

                await ctx.reply(embed=embed)
                break


async def setup(client):
    await client.add_cog(Republish(client))
        
        