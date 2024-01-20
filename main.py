import os
import json
import logging
from src.app        import monitor
from src.config     import cfg_file


logging.basicConfig(
    level=logging.DEBUG if cfg_file["other"]["debug_mode"] else logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
    handlers=[
        logging.FileHandler("rodrobe.log",encoding="utf8"),
        logging.StreamHandler()
    ]
)


def create_config(file_path, dump_obj={}):
    if not os.path.isfile(file_path):
        print(file_path)
        with open(file_path, "a") as file:
            json.dump(dump_obj, file)


create_config("src/cache/config.json")
create_config("src/cache/cached_ids.json", dump_obj={"ids": []})


def main():
    """
    Initiates the program 
    """

    logger = logging.getLogger(__name__)

    logger.info("Starting RoDrobe v1.6")

    if not os.path.isfile("config/description.txt"):
        with open("config/description.txt","a") as file:
            file.write("\n")

    try:
        new_monitor = monitor.Monitor(
            holder_cookie=cfg_file["group"]["holder_cookie"],
            uploader_cookie=cfg_file["group"]["uploader_cookie"],
            group_id=cfg_file["group"]["group_id"],
        )
        new_monitor.load()

    except Exception as exception:
        logger.error(exception)


if __name__ == "__main__":
    main()
