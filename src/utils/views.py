import os
import discord 

from src.utils import assets
from src       import config

class DownloadView(discord.ui.View):

    def __init__(self, asset_id: int, embed):
        super().__init__()

        self.embed = embed
        self.asset_id = asset_id

    @discord.ui.button(label = "Remove Watermark", style=discord.ButtonStyle.blurple)
    async def removeWatermark(self, interaction: discord.Interaction, button:  discord.ui.Button):
        button.disabled = True
        nwFile = assets.stripAssetWatermark(self.asset_id)["file"]

        # just incase
        if not nwFile:

            embed = discord.Embed(
                title="Error",
                color=config.EmbedColors.ERROR,
                description="Asset type is not supported\nOnly shirts and pants can have their watermark removed."
            )
            await interaction.response.send_message(embed=embed,ephemeral= True) 
            return           

        file = discord.File(nwFile,filename="asset.png")
        self.embed.set_image(url="attachment://asset.png")

        
        await interaction.response.edit_message(view = self,embed=self.embed, attachments = [file])
        os.remove(nwFile)
    
