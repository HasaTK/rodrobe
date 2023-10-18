import os 
import dotenv
import json

from src.utils      import log
from toml           import load
from src.exceptions import InvalidConfigException

cfg_file = load(".toml")


class EmbedColors:

    ERROR = 0xcd2934
    SUCCESS = 0x00ff6e
    INFO = 0x4aafed


if not os.path.isfile("src/cache/config.json"):
    with open("src/cache/config.json","a") as file:
        json.dump({},file)


def is_whitelisted(user: any):
    """ 
    Check if a user is allowed to use the bot

    :param any user:
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
     


