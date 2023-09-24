import discord 
import requests
import os 

from src.utils      import log, assets
from src.exceptions import InvalidAssetId
from discord.ext    import commands 

from hashlib            import sha256
from src.config         import EmbedColors
from src.utils.views    import DownloadView





class Download(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        log.success("Downlad cog is ready")
    
    
    @commands.command(help = f"Shows template of an asset")
    async def download(self, ctx, asset_id):        
        try:

            assetBytes = assets.fetchAssetBytes(asset_id=asset_id)
            file_name = sha256(str(asset_id).encode("utf-8")).hexdigest() + ".png"
            with open(f"src/cache/{file_name}","wb") as file:
                file.write(assetBytes['bytes'])

            
            asset_details = assets.getAssetDetails(asset_id)
            embed_description = f"**Type:** {assetBytes['type']}\n**Asset:** [{asset_details['name'] if asset_details else 'asset_name'}](https://www.roblox.com/catalog{asset_id})"
            

            if asset_details:
                #TODO: rewrite this
                creator_id = str(asset_details['creatorTargetId'])
                embed_description += f"\n**Creator:** [{asset_details['creatorName']}]({'https://www.roblox.com/users/'+creator_id+'/profile' if asset_details['creatorType'] == 'User' else 'https://www.roblox.com/groups/'+creator_id})"
            
            embed = discord.Embed(
                title = "Download",
                color=EmbedColors.SUCCESS,
                description=embed_description
            )

            file = discord.File(f"src/cache/{file_name}",filename="asset.png")
            embed.set_image(url="attachment://asset.png")

            
            if str(assetBytes['type']).lower()  in ('shirt','pants'):
                view = DownloadView(asset_id = asset_id, embed = embed)
            else:
                view = None
            
            await ctx.reply(embed=embed, file=file, view = view)

            os.remove(f"src/cache/{file_name}")
            
        except InvalidAssetId:
            await ctx.reply("Asset id provided is invalid")
        except Exception as e:
            print(e)
            await ctx.reply("Error while attempting to run command.")


async def setup(client):
    await client.add_cog(Download(client))
        
        