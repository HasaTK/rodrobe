import requests
from src.exceptions import InvalidGroupID


def getGroupInfo(group_id: int):
    """
    Gets info on the group id provided 

    :param int group_id
    :return: info
    """

    groupInfo = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}")

    if "group is invalid or does not exist" in str(groupInfo.text).lower():
        raise InvalidGroupID("Group ID provided is invalid")

    return groupInfo.json()
