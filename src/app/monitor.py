import requests
import time
import asyncio
import threading
import random
import logging 

from src.utils.currency import robux_price
from src.clients        import accounts
from src.exceptions     import InvalidCredentialsError, AccountNotInGroup, LowRankException
from src                import config
from src.adapters       import webhooks
from src.clients        import discord


def start_discord_bot():

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(discord.main())


class Monitor:

    def __init__(
        self, 
        holder_cookie:   str, 
        uploader_cookie: str,
        group_id:        int
    ):

        self.active = False
        self.cookies = (holder_cookie, uploader_cookie)
        self.group_id = group_id

        self.holder = accounts.RobloxAccount(self.cookies[0])
        self.uploader = accounts.RobloxAccount(self.cookies[1])
        self.last_cached_id = None

        self.sales_webhook = webhooks.DiscordWebhook() if config.cfg_file["discord"]["sales_webhook"] else None
        self.logger = logging.getLogger(__name__)
        
    def verifyGroupRankings(self):

        self.logger.info("Checking if accounts are in specified group..")
        holder_data   = self.holder.checkIfInGroup(self.group_id)
        uploader_data = self.uploader.checkIfInGroup(self.group_id)

        if not holder_data:
            raise AccountNotInGroup(f"{self.holder.name} is not in the specified group ID ({self.group_id})")
        if not uploader_data:
            raise AccountNotInGroup(f"{self.uploader.name} is not in the specified group ID ({self.group_id})")
        
        if not holder_data["isOwner"]:
            raise LowRankException(f"{self.holder.name} is not an owner in the specified group ID ({self.group_id})")
        
    

    def fetchNewSales(self):

        params = {
            "cursor":None,
            "limit": 25,
            "transactionType":"Sale"
        }
        self.logger.debug("Checking for new sales..")

        salesPage = requests.get(
            url=f"https://economy.roblox.com/v2/groups/{self.group_id}/transactions",
            params=params,
            headers=self.holder.headers
        )

        salesData= salesPage.json()["data"]
        if not salesData:
            return

        if salesData[0]["id"] == self.last_cached_id:

            self.logger.debug("Checked for sales with 0 new sales found.")
            return 

        if self.last_cached_id:
            newSalesCache = []

            for sale in salesData:
                if sale["details"]["type"] == "Asset":
                    if sale["id"] == self.last_cached_id:
                        self.last_cached_id = salesData[0]["id"]
                        return 

                    rates = config.cfg_get("rates") or 3.5

                    robuxAT = sale['currency']['amount']
                    robuxBT = sale['currency']['bt_amount'] = robuxAT / 0.7 

                    newSalesCache.append(sale)
                    self.logger.info(f"Fetched new sale for {sale['details']['name']} by {sale['agent']['name']} ({robuxAT} A/T)")

                    if self.sales_webhook:
                        get_player_headshot = requests.get(
                            url=f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={sale['agent']['id']}",
                            params={
                                "size": "150x150",
                                "format": "Png",
                                "isCircular": False
                            }
                        )
                        if get_player_headshot.ok:
                            player_headshot = get_player_headshot.json()["data"][0]["imageUrl"]
                        else:
                            player_headshot = "https://t6.rbxcdn.com/b48637b2a6266bd379a09afb5a8d5131"

                        self.sales_webhook.raw_send(content={
                            "content": "",
                            "embeds":[
                                {
                                    "type": "rich",
                                    "title": "New Item Sold 💰",
                                    "description": "",
                                    "color": 0x0fbb7f,
                                    "fields":[
                                        {
                                            "name": "Player",
                                            "value": f"**Username: [{sale['agent']['name']}](https://www.roblox.com"
                                                     f"/users/{sale['agent']['id']}/profile)**\n**"
                                                     f"User ID: {str(sale['agent']['id'])}**"
                                        },
                                        {
                                            "name": "Item",
                                            "value": f"**[{sale['details']['name']}](https://www.roblox.com/catalog/{str(sale['details']['id'])})**"
                                        },
                                        {
                                            "name": "Amount",
                                            "value": f"**A/T: {robuxAT} (${robux_price(robuxAT,rates)})**\n**B/T: "
                                            f"{round(robuxBT)} (${robux_price(robuxBT, rates)})**"
                                        }
                                    ],
                                    "thumbnail": {
                                        "url": player_headshot,
                                        "proxy_url": player_headshot,
                                    },
                                    "footer": {
                                        "text": f"Currency converted using rates: ${rates} / 1k (2DP)"
                                    },
                                }
                            ]
                        })

        self.last_cached_id = salesData[0]["id"]

    def load(self):
        """
        Loads the Monitor 
        """

        holder_info   = self.holder.getClientInfo()
        uploader_info = self.uploader.getClientInfo()

        if not holder_info:
            raise InvalidCredentialsError("Holder cookie is invalid")
        else:
            self.logger.info(f"Logged in to {holder_info['name']} ({holder_info['id']}) (holder)")

        if not uploader_info:
            raise InvalidCredentialsError("Uploader cookie is invalid")
        else:
            self.logger.info(f"Logged in to {uploader_info['name']} ({uploader_info['id']}) (uploader)")
        
        try:
            self.verifyGroupRankings()
        except Exception as e:
            self.logger.error(e)
            return

        threading.Thread(target=start_discord_bot, args=(),).start()

        while True:
            try:
                self.fetchNewSales()
            except Exception as e:
                self.logger.error("FETCHER {}".format(e))
            
            time.sleep(random.randint(30, 60))

        