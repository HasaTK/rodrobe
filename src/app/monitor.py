import requests
import time, random

from typing             import Optional,Dict,List

from src.utils          import log
from src.utils.currency import robux_price
from src.clients        import accounts
from src.exceptions     import InvalidCredentialsError, AccountNotInGroup, LowRankException
from src                import config
from src.adapters       import webhooks



class Monitor:

    def __init__(
        self, 
        holder_cookie:   str, 
        uploader_cookie: str,
        group_id:        int
    ):

        self.active = False
        self.cookies = (holder_cookie,uploader_cookie)
        self.group_id = group_id

        self.holder = accounts.RobloxAccount(self.cookies[0])
        self.uploader = accounts.RobloxAccount(self.cookies[1])
        self.last_cached_id = None

        self.sales_webhook = webhooks.DiscordWebhook() if config.get("discord_webhook") else None
        
    def verifyGroupRankings(self):

        log.info("Checking if accounts are in specified group..")
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
        log.info("Checking for new sales..")

        salesPage = requests.get(f"https://economy.roblox.com/v2/groups/{self.group_id}/transactions",params=params,headers=self.holder.headers)
        salesData= salesPage.json()["data"]
        print(salesPage.status_code)

        if salesData[0]["id"] == self.last_cached_id:

            log.info("Checked for sales with 0 new sales found.")
            return 
        
        
        if self.last_cached_id:
            newSalesCache = []

            for sale in salesData:
                if sale["details"]["type"] == "Asset":
                    if sale["id"] == self.last_cached_id:
                        self.last_cached_id = salesData[0]["id"]
                        return 

                    #TODO: Recode this
                    rates = config.cfg_get("rates") or 3.5

                    robuxAT = sale['currency']['amount']
                    robuxBT = sale['currency']['bt_amount'] = robuxAT / 0.7 

                    newSalesCache.append(sale)
                    log.success(f"Fetched new sale for {sale['details']['name']} by {sale['agent']['name']} ({robuxAT} A/T)")

                    if self.sales_webhook:
                        get_player_headshot = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={sale['agent']['id']}&size=150x150&format=Png&isCircular=false")
                        if not get_player_headshot.ok:
                            player_headshot = "https://t6.rbxcdn.com/b48637b2a6266bd379a09afb5a8d5131"
                        else:
                            player_headshot = get_player_headshot.json()["data"][0]["imageUrl"]
                            

                        self.sales_webhook.raw_send(content={
                            "content":"",
                            "embeds":[
                                {
                                    "type":"rich",
                                    "title":"New Item Sold 💰",
                                    "description":"",
                                    "color": 0x0fbb7f,
                                    "fields":[
                                        {"name":"Player","value":f"**Username: [{sale['agent']['name']}](https://www.roblox.com/users/{sale['agent']['id']}/profile)**\n**User ID: {str(sale['agent']['id'])}**"},
                                        {"name":"Item","value":f"**[{sale['details']['name']}](https://www.roblox.com/catalog/{str(sale['details']['id'])})**"},
                                        {"name":"Amount","value":f"**A/T: {robuxAT} (${robux_price(robuxAT,rates)})**\n**B/T: {round(robuxBT)} (${robux_price(robuxBT, rates)})**"}
                                    ],
                                    "thumbnail":{
                                        "url": player_headshot,
                                        "proxy_url":player_headshot,
                                    },
                                    "footer":{
                                        "text":f"Currency converted using rates: ${rates} / 1k (2DP)"
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
            log.success(f"Logged in to {holder_info['name']} ({holder_info['id']})")

        if not uploader_info:
            raise InvalidCredentialsError("Uploader cookie is invalid")
        else:
           log.success(f"Logged in to {uploader_info['name']} ({uploader_info['id']})")
        
        try:
            self.verifyGroupRankings()
        except Exception as e:
            log.error(e)
            return 

        while True:
            try:
                self.fetchNewSales()
            except Exception as e:

                log.error(e, prefix="fetcher")
            
            time.sleep(random.randint(30,60))

        