import multiprocessing
import asyncio, os

from src.app        import monitor
from src.utils      import log
from src            import config

from src.clients import discord
from multiprocessing import Process

def main():
    """
    Initiates the program 
    """
    
    log.info("Starting program..")

    if not os.path.isfile("config/description.txt"):
        log.error("Please create a text file called 'description' in the config folder. This file will be used when assets are being uploaded.")
        return
    newMonitor = monitor.Monitor(
        holder_cookie   = config.get("holder_cookie"),
        uploader_cookie = config.get("uploader_cookie"),
        group_id        = config.get("group_id"),
    )

    Process(target=newMonitor.load,args=()).start()
    asyncio.run(discord.main())


if __name__ == "__main__":
    main()