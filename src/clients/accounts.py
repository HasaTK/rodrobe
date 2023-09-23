import requests

from src.utils              import log 
from requests.exceptions    import JSONDecodeError
from typing import Optional, Dict


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
        
        

    def getGroupAssets(self, group_id: int, limit: Optional[int] = 50):

        """ 
        Fetches the ids of the assets in the specified group up to the specified limit

        :param int group_id:
        :param Optional limit:

        :return: list of fetched ids
        :rtype: list
        """

        fetchData = requests.get(
            "https://catalog.roblox.com/v1/search/items",
            params={
                "category":"Clothing",
                "creatorTargetId":group_id,
                "creatorType":"Group",
                "cursor":None,
                "limit":limit,
                "sortOrdder":"Desc"
            },
            headers=self.headers
        )
        
        cached_assets = []

        log.info(fetchData.status_code)

        if fetchData.ok:
            data = fetchData.json()["data"]
            for asset in data:
                if asset["itemType"] == "Asset":
                   cached_assets.append(asset["id"])

        
        
        return cached_assets

                
