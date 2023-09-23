from src.app    import monitor
from src.utils  import log
from src        import config


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

    newMonitor.load()

if __name__ == "__main__":
    main()