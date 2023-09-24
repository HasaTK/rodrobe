import multiprocessing
import asyncio

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


    newMonitor = monitor.Monitor(
        holder_cookie   = config.get("holder_cookie"),
        uploader_cookie = config.get("uploader_cookie"),
        group_id        = config.get("group_id"),
    )

    Process(target=newMonitor.load,args=()).start()
    asyncio.run(discord.main())


if __name__ == "__main__":
    main()