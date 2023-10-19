import os

import logging
from src.app        import monitor
from src.config     import cfg_file
from toml           import load


logging.basicConfig(
    level=logging.DEBUG if cfg_file["other"]["debug_mode"] else logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
    handlers=[
        logging.FileHandler("rodrobe.log"),
        logging.StreamHandler()
    ]
)


def main():
    """
    Initiates the program 
    """

    logger = logging.getLogger(__name__)

    config = load(".toml")
    logger.info("Starting program..")
    if not os.path.isfile("config/description.txt"):
        logger.error("Create a text file called 'description' in the config folder. This file will be used when assets are being uploaded. ")
        return

    try:
        new_monitor = monitor.Monitor(
            holder_cookie   = config["group"]["holder_cookie"],
            uploader_cookie = config["group"]["uploader_cookie"],
            group_id        = config["group"]["group_id"],
        )
        new_monitor.load()

    except Exception as exception:
        logger.error(exception)


if __name__ == "__main__":
    main()
