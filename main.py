import os
import asyncio
from src.app        import monitor
from src.utils      import log
from toml           import load
from multiprocessing import Process

from src.clients import discord


def main():
    """
    Initiates the program 
    """

    config = load(".toml")
    log.info("Starting program..")

    if not os.path.isfile("config/description.txt"):
        log.error("Please create a text file called 'description' in the config folder. This file will be used when assets are being uploaded.")
        return

    try:
        new_monitor = monitor.Monitor(
            holder_cookie   = config["group"]["holder_cookie"],
            uploader_cookie = config["group"]["uploader_cookie"],
            group_id        = config["group"]["group_id"],
        )
        Process(target=new_monitor.load, args=()).start()
        asyncio.run(discord.main())

    except Exception as exception:
        log.error(exception)


if __name__ == "__main__":
    main()
