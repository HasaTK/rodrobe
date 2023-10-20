import os 
import json

from toml import load
from typing import Any

cfg_file = load(".toml")


class EmbedColors:

    ERROR = 0xcd2934
    SUCCESS = 0x00ff6e
    INFO = 0x4aafed



def is_whitelisted(user: Any):
    """ 
    Check if a user is allowed to use the bot

    :param Any user:
    :return: bool
    """

    wl_table = cfg_file["discord"]["bot_whitelist"]

    if type(user) == int:
        return id in wl_table
    else:
        return user.author.id in wl_table


def cfg_set(key, value):

    """ 
    Sets a value of the specified key from the cache config
    
    :param str key:
    :param value:


    """
    with open("src/cache/config.json","r+") as file:
        jfile  = json.load(file)
        jfile[key] = value
        file.seek(0)
        json.dump(jfile, file)
        file.truncate()


def cfg_get(key: str):
    """ 
    Returns the value of a key from the cache config
    
    :param str key: Name of the key
    :return: value

    """
    with open("src/cache/config.json","r") as file:
        jfile  = json.load(file)

        if jfile.get(key):
            return jfile[key]
        else:
            return None


def is_cached(asset_id: int) -> bool:
    with open("src/cache/cached_ids.json") as file:
        jfile = json.load(file)

    return asset_id in jfile["ids"]


