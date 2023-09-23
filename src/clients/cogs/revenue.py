import discord 

from src                    import config
from src.clients            import accounts
from src.utils              import log, groups
from src.utils.currency     import robux_price
from discord.ext            import commands 

class revenue(commands.Cog):

    def __init__(self, client):
        self.client         = client 
        self.holder_account = accounts.RobloxAccount(config.get("holder_cookie"))
        self.group_id = config.get("group_id")

    @commands.Cog.listener()
    async def on_ready(self):
        log.success("Revenue cog is ready")
    
    @commands.command(aliases=["robux","bal","balance"])

    async def revenue(self, ctx):

        rates = config.cfg_get("rates") or 3.5

        group_info = groups.getGroupInfo(self.group_id)
        group_summary = self.holder_account.getGroupSummary(self.group_id)

        verified_robux = group_summary['robux']
        pending_robux  = group_summary['pending_robux']
        total_robux    = verified_robux + pending_robux

        embedBuild = discord.Embed(
            title = f"{group_info['name']} Balance",
            description = f"**Verified Robux:** {verified_robux} (${robux_price(verified_robux,rates)})\n**Pending Robux:** {group_summary['pending_robux']} (${robux_price(pending_robux,rates)})\n**Total(Pending + Verified):** {total_robux} (${robux_price(total_robux,rates)})",
            color = 0x0cb994
        )

        embedBuild.set_footer(text=f"Currency converted using rates: ${rates} / 1k (2DP)")

        await ctx.reply(embed=embedBuild)


async def setup(client):
    
    await client.add_cog(revenue(client))
        
        