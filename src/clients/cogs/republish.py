import discord 
import requests

from hashlib        import sha256
from src.utils      import log,assets
from src.utils      import groups
from src.exceptions import InvalidAssetId, InvalidAssetType, AssetDetailsNotFound, InvalidGroupID

from src.clients    import accounts
from discord.ext    import commands 
from src            import config

class Republish(commands.Cog):

    def __init__(self, client):
        self.client = client 
        self.uploader = accounts.RobloxAccount(config.get("uploader_cookie"))

    def republish_asset(self, asset_id: int, remove_watermark = True):

        if remove_watermark:
            asset = assets.stripAssetWatermark(asset_id=asset_id)
            if not asset:
                # most likely a  tshirt
                return self.republish_asset(asset_id=asset_id, remove_watermark=False)
            asset_path = asset["file"]
                    
        else:

            asset = assets.fetchAssetBytes(asset_id)
            asset_path = "src/cache/" + str(sha256(str(asset_id).encode("utf-8")).hexdigest()) + ".png"
            
            with open(asset_path, "wb") as file:
                file.write(asset["bytes"])
            print(2)
            
        asset_details = assets.getAssetDetails(asset_id)
        if not asset_details:
            raise AssetDetailsNotFound("Asset details were unable to be obtained")
                
        
        if asset["type"].lower() == "shirt graphic" or asset["type"] == "TShirt":
            asset_type = "TShirt"
        elif asset:
            asset_type = asset["type"].lower().capitalize()

        if not asset_type.lower() in ("shirt","pants","tshirt"):
            raise InvalidAssetType("Asset Type provided is not valid")

        republish = self.uploader.uploadGroupAsset(
            group_id=config.get("group_id"), 
            asset_type = asset_type, 
            asset_name = asset_details["name"], 
            bin_file = open(asset_path,"rb"),
        )
        
        return republish

        
 
        

    @commands.Cog.listener()

    async def on_ready(self):
        log.success("Republishing cog is ready")
    
    @commands.command(help="uploads the asset to your own group", aliases = ["republish", "repub", "rp", "rb"])
    @commands.check(config.is_whitelisted)

    async def steal(self, ctx, asset_id, remove_watermark = True):
        try:
            init_embed = discord.Embed(
                title = f"Attempting to republish asset ",
                color =  config.EmbedColors.INFO
            )

            message = await ctx.reply(embed=init_embed)
            repubAsset = self.republish_asset(asset_id=asset_id,remove_watermark=remove_watermark)
            if repubAsset:

                pub_id = repubAsset["response"]["assetId"] 

                embed = discord.Embed(
                    title = "Republished asset successfully",
                    color = config.EmbedColors.SUCCESS,
                    description = f"The republished asset can be found [here](https://www.roblox.com/catalog/{pub_id})"
                )

                await message.edit(embed = embed)

        except InvalidAssetId:
            
            embed = discord.Embed(
                title = "Invalid Asset Id",
                color = config.EmbedColors.ERROR,
                description = "The asset id provided is invalid"
            )

            await message.edit(embed = embed)
        
        except AssetDetailsNotFound:

            log.error("Asset details were not found",__name__)
            embed = discord.Embed(
                title = "Error",
                color = config.EmbedColors.ERROR,
                description = "Error while attempting to attemping to get asset details."
            )

            await message.edit(embed=embed)
        except InvalidAssetType:
            embed = discord.Embed(
                title = "Invalid Asset Type",
                color = config.EmbedColors.ERROR,
                description = "The asset type provided is invalid"
            )

            await message.edit(embed = embed)
         
        except Exception as e:
            
            log.error(e,__name__)
            embed = discord.Embed(
                title = "Error",
                description=f'```{e}```',
                color= config.EmbedColors.ERROR
        
            )

            await message.edit(embed = embed)
                


    
    @commands.command(help="republishes all the assets an existing group has to your group", aliases = ["sg", "stealgroup", "rg", "republishgroup","repgroup","repg"])
    @commands.check(config.is_whitelisted)

    async def sgroup(self, ctx, group_id, remove_watermark = True):
        
        try: 
            group_info = groups.getGroupInfo(group_id=group_id)
        except InvalidGroupID:
            embed = discord.Embed(
                title = "Invalid group ID",
                description="The group id provided is invalid",
                color = config.EmbedColors.ERROR
            )

            await ctx.reply(embed = embed)

        warningEmbed = discord.Embed(
            title = "Confirmation",
            description=f"Are you sure you want to upload all clothing assets from group [{group_id}](https:/www.roblox.com/groups/{group_id})"
        )

        uploader = accounts.RobloxAccount(config.get("uploader_cookie"))
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
                            upload = self.republish_asset(asset_id=asset["id"], remove_watermark=remove_watermark)
                            if upload:
                                upload_count += 1

                                pub_id = upload["response"]["assetId"] 
                                pub_name = upload["response"]["displayName"]
                                log.info(f"Uploaded asset  of '{pub_name}' with id: {pub_id}")
                                
                                publishEmbed = discord.Embed(
                                    title = "Last asset published",
                                    description = f"Last published [{pub_name}](https:/www.roblox.com/catalog/{pub_id})",
                                    color = config.EmbedColors.INFO
                                )
                                await message.edit(embed=publishEmbed)
                            else:
                                log.error(upload,__name__)
                    
                    else:
                        if "the creator does not have enough robux to pay for the upload fees" in str(request.text).lower():
                            embed = discord.Embed(
                                title="Report",
                                color=config.EmbedColors.ERROR,
                                description=f"A total of {upload_count} assets were uploaded before running out of robux."
                                )
                            await ctx.reply(embed=embed)
                        elif "user is moderated" in str(request.text).lower():
                            embed = discord.Embed(
                                title="Report",
                                color=config.EmbedColors.ERROR,
                                description=f"A total of {upload_count} assets were uploaded before being terminated."
                            )

                            await ctx.reply(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="Report",
                                color=config.EmbedColors.ERROR,
                                description=f"A total of {upload_count} assets were before encountering an error.\nError:\n```{request.text}"
                            )

                            await ctx.reply(embed=embed)

                    
                    cached_assets = uploader.getGroupAssets(group_id=group_id, cursor=cached_assets["obj"]["nextPageCursor"])
                else:
                    break

                        
                    
            except Exception as e:
                embed = discord.Embed(
                    title = "Error",
                    description=f'```{e}```',
                    color= config.EmbedColors.ERROR
        
                )

                await ctx.reply( embed = embed)
                break

            



async def setup(client):
    await client.add_cog(Republish(client))
        
        