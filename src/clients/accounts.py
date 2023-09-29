import time
import requests
import json,uuid
import os

from src                    import config
from src.utils              import log 
from src.exceptions         import InvalidAssetType, InsufficientFundsException
from requests.exceptions    import JSONDecodeError
from typing import Optional, Dict


from pprint import pprint
class RobloxAccount():
    
    def __init__(
        self,
        cookie,
        user_agent: Optional[str] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    ):

        self.cookie     = ".ROBLOSECURITY="+cookie
        self.user_id    =  None
        self.user_agent = user_agent 
        self.headers    = {"User-Agent":self.user_agent, "Cookie": self.cookie}
        self.csrf_token = self.getCsrfToken()
        self.getClientInfo()

     
    def getClientInfo(self) -> Dict:

        """
        Gets & initializes user id and name of the client and returns it in a dict

        :return: {"id":id_here,"name":name_here}
        :rtype:  dict
        """

        client_info = requests.get("https://www.roblox.com/my/settings/json", headers=self.headers)
        
        try: 
        
            self.user_id =  client_info.json()["UserId"]
            self.name   =  client_info.json()["Name"]

            return {
                "id": self.user_id,
                "name": self.name
            }

        except Exception as err:
            log.error(f"Failed to get account info | {err}")
            return False
    

    def getRobux(self) -> int:
        """
        Gets amount of robux  
        
        :return robux:
        :rtype int:
        """

        client_robux = requests.get(f"https://economy.roblox.com/v1/users/{self.user_id}/currency", headers=self.headers)
        return client_robux.json()["robux"]

    
    def getAllGroups(self) -> Dict:
        """
        Gets the groups the account is in along with the roles the account has

        :return: groups & roles
        :rtype dict:
        """
        
        group_roles = requests.get(f"https://groups.roblox.com/v1/users/{self.user_id}/groups/roles", headers = self.headers)
        return group_roles.json()

    
    def checkIfInGroup(self, group_id: int) -> dict:
        """
        Checks if the account is in the specified group id and returns a self explanatory dictionary

        return dict:
        {
            "isOwner": bool, 
            "rank": int,
        }

        If the accout is not in the specified group then it will return a NoneType
        
        :param int group_id:
        :return: dict
        :rtype int | bool:
        """

        groupsData = self.getAllGroups()["data"]
        if not groupsData:
            return None
            
        for group in groupsData:
            group_obj = group["group"]
            
            if group_obj["id"] == group_id:
                role_obj = group["role"]

                if self.user_id == group_obj["owner"]["userId"]:
                    return {"isOwner":True,"rank":role_obj["rank"]}
                else:
                    return {"isOwner":False,"rank":role_obj["rank"]}    
        return None

    def getGroupSummary(self, group_id: int):
        

        group_bal = requests.get(f"https://economy.roblox.com/v1/groups/{group_id}/currency",headers = self.headers)
        summary = requests.get(f"https://economy.roblox.com/v1/groups/{group_id}/revenue/summary/day",headers = self.headers)

        if group_bal.ok and summary.ok:
            return {"robux":group_bal.json()["robux"], "pending_robux": summary.json()["pendingRobux"]}
        
    
    def getCsrfToken(self):

        """ 
        Generates an x-csrf-token

        :return token:
        """

        get_token = requests.post("https://auth.roblox.com/v2/logout",headers=self.headers)

        # TOOD: use json.loads/load
        if "x-csrf-token" in str(get_token.headers).lower():
            return get_token.headers["x-csrf-token"]
        else:
            log.error(f"Error fetching x-csrf-token | {get_token.status_code} | {get_token.text}",__name__)
            return None

    def getGroupAssets(self, group_id: int, limit: Optional[int] = 50, cursor: Optional[str] = None):

        """ 
        Fetches the ids of the assets in the specified group up to the specified limit

        :param int group_id:
        :param Optional limit:
        :param Optional cursor:

        :return: list of fetched ids
        :rtype: list
        """

        fetchData = requests.get(
            "https://catalog.roblox.com/v1/search/items",
            params={
                "category":"Clothing",
                "creatorTargetId":group_id,
                "creatorType":"Group",
                "cursor":cursor,
                "limit":limit,
                "sortOrder":"Desc"
            },
            headers=self.headers
        )
        
        cached_assets = []
        log.info(fetchData.status_code)

        if fetchData.ok:
            data = fetchData.json()["data"]
            for asset in data:
                if asset["itemType"] == "Asset":
                   cached_assets.append(asset)

        
        
        return {"data":cached_assets,"obj":fetchData}

    
    def releaseAsset(self, asset_id: int, price: int):

        """ 
        Releases an asset/ puts it on sale

        :param int asset_id:
        :param int price:

        """

        headers = self.headers
        headers["x-csrf-token"] = self.csrf_token

        release_request = requests.post(
            f"https://itemconfiguration.roblox.com/v1/assets/{asset_id}/release",
            json={
                "priceConfiguration":{
                    "priceInRobux":price
                },
                "saleStatus":"OnSale",
                "releaseConfiguration":{
                    "saleAvailabilityLocations":[0,1]
                }
            },
            headers = headers
        )


        if not release_request.ok:
            raise Exception(release_request.text)
        return release_request

    def uploadGroupAsset(self, group_id: int, asset_type: str, asset_name: str, bin_file):

        """ 
        Uploads an asset  to a group 
        
        :param int group_id:
        :param str asset_type:
        :param str asset_name:
        :param bin_file: 
        """

        headers = self.headers
        headers["x-csrf-token"] = self.csrf_token
        headers["Accept"] = "*/*"
        headers["Pragma"] =  "no-cache"
        headers["Origin"] = "create.roblox.com"
        headers["Referer"] = "https://create.roblox.com/"

        if str(asset_type) not in ("Shirt","Pants","TShirt"):
            raise InvalidAssetType("Asset type provided is invalid. Double check capitalization")
        else:
            rel_price = config.get("tshirt_price") if asset_type == "TShirt" else config.get("item_price")
            expectedPrice = 0 if asset_type== "TShirt" else 10
       
        with open("config/description.txt","r") as file:
            description = file.read()

        request_data = json.dumps({"displayName":asset_name,"description":description,"assetType":asset_type,"creationContext":{"creator":{"groupId":group_id},"expectedPrice":expectedPrice}})
        
        upload_req = requests.post(
            "https://apis.roblox.com/assets/user-auth/v1/assets",
            headers = headers,
            files = {"fileContent":(bin_file.name, bin_file,"image/png"),"request":(None,request_data)},
        )


        if upload_req.ok:
            while True:
                op_lookup = requests.get(f"https://apis.roblox.com/assets/user-auth/v1/{upload_req.json()['path']}",headers = headers)

                if op_lookup.ok: 
                    #print(op_lookup.ok)
                    if op_lookup.json().get("done"):
                        asset_id =  op_lookup.json()["response"]["assetId"]
                        release_item = self.releaseAsset(asset_id=asset_id, price= rel_price)
                        return op_lookup.json()
                
             
                    
        else:
            if "InsufficientFunds" in upload_req.text:
                raise InsufficientFundsException(upload_req.json())

            return False
