import os
import discord 
from src.utils import assets

class DownloadView(discord.ui.View):

    def __init__(self, asset_id: int, embed):
        super().__init__()

        self.embed = embed
        self.asset_id = asset_id

    @discord.ui.button(label = "Remove Watermark", style = discord.ButtonStyle.blurple)
    async def removeWatermark(self, interaction:discord.Interaction, button:discord.ui.Button):
        button.disabled = True
        nwFile = assets.stripAssetWatermark(self.asset_id)

        file = discord.File(nwFile,filename="asset.png")
        self.embed.set_image(url="attachment://asset.png")

        
        await interaction.response.edit_message(view = self,embed=self.embed, attachments = [file])
        os.remove(nwFile)
        