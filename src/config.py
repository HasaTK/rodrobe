import os 
import dotenv
import json

from src.utils      import log
from dotenv         import load_dotenv
from src.exceptions import InvalidConfigException

load_dotenv(".env")

cfg_tuple = (
    "group_id",
    "holder_cookie",
    "uploader_cookie",
    "discord_webhook",
    "discord_bot_token",
    "discord_bot_prefix"
)

if not os.path.isfile("src/cache/config.json"):
    with open("src/cache/config.json","a") as file:
        json.dump({},file)

def get(requested_item) -> str | int:
    """ 
    Gets the config requested

    :param str requested_item:
    :return: 
    :rtype str | int:
    """

    if requested_item.lower() in cfg_tuple:
        item = os.environ.get(requested_item.upper())
        if item:
            if item.isnumeric():
                return int(item)
            else:
                return item
    
    raise InvalidConfigException("Config does not exist or is not able to be accessed.")


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
     


