import requests

def getGroupInfo(group_id: int):
    groupInfo = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}")
    return groupInfo.json()
    