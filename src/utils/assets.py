import requests
import re
import logging
import os
import time
import uuid

from hashlib        import sha256
from PIL            import Image
from src.exceptions import InvalidAssetId, AssetDetailsNotFound, InvalidAssetType
from src.config     import cfg_file
from typing import Optional, Dict, Any

x_csrf_token = "wXbG1Fd"
logger = logging.getLogger(__name__)


def fetchAssetBytes(asset_id: int):
    """ 
    Fetches the asset bytes

    :param int asset_id:
    :return: bytes

    """    

    asset_xml = requests.get(f"https://assetdelivery.roblox.com/v1/asset?id={asset_id}")

    if asset_xml.ok:
        rId = ((re.findall(r'<url>(.+?)(?=</url>)',asset_xml.text)[0])
               .replace("http://www.roblox.com/asset/?id=", "")
               .replace("?version=1&amp;", "")
               .replace("http://www.roblox.com/asset/id=", ""))

        rType = re.findall(r'<string name="Name">(.+?)(?=</string>)', asset_xml.text)[0]
        assetData = requests.get(f"https://assetdelivery.roblox.com/v1/assetId/{rId}")

        fbytes = requests.get(assetData.json()["location"]).content

        return {"type": rType,"bytes": fbytes}
    else:
        raise InvalidAssetId("Asset ID is invalid")


def getAssetDetails(asset_id: int, csrf_token: Optional[str] = None):
    global x_csrf_token
    """ 
    Fetches the details of the asset
    
    :param int asset_id:
    :param Optional csrf_token:

    :return: details
    """

    details = requests.post(
        url="https://catalog.roblox.com/v1/catalog/items/details",
        json={"items": [{"id":asset_id, "itemType": "asset"}]},
        headers={
            "content-type":"application/json",
            "x-csrf-token":csrf_token or x_csrf_token
        }
    )

    if details.status_code == 403 and "Token Validation Failed" in details.text:
        x_csrf_token = details.headers["x-csrf-token"]
        return getAssetDetails(asset_id, x_csrf_token) # TODO:  cache the token and/or use sessions??

    elif details.ok:
        return details.json()['data'][0]

    elif details.status_code == 429:
        logger.warning("Ratelimited whilst attempting to grab asset details. Retrying...")
        time.sleep(cfg_file["other"]["ratelimit_wait_time"] or 5)
        return getAssetDetails(asset_id=asset_id, csrf_token=x_csrf_token)
    else:
        return None


def getGroupedAssetDetails(asset_list, csrf_token: Optional[str] = None):
    global x_csrf_token

    """ 
    Fetches the details of numerous assets

    :param asset_list: e.g: [{"id":1,"itemType":"Asset"}, ...]
    :param Optional csrf_token:

    :return: details
    """

    headers = {
        "content-type": "application/json",
        "x-csrf-token": csrf_token or x_csrf_token
     }

    request = requests.post(
        url="https://catalog.roblox.com/v1/catalog/items/details",
        json={"items": asset_list},
        headers=headers
    )

    if request.ok:
        return request.json()
    
    elif request.status_code == 403 and "Token Validation Failed" in request.text:
        x_csrf_token = request.headers["x-csrf-token"]
        return getGroupedAssetDetails(asset_list=asset_list, csrf_token=x_csrf_token)
    else:
        return False


def stripAssetWatermark(asset_id: int):
    """
    Removes watermark from asset

    :param asset_id:
    :return: path to stripped image
    """

    asset_bytes = fetchAssetBytes(asset_id)
    file_name = f"src/cache/{str(uuid.uuid4())}.png"

    with open(file_name,"wb") as file:
        
        file.write(asset_bytes["bytes"]) 
    
    asset = Image.open(file_name)
    asset_type = str(asset_bytes["type"]).lower() 

    if asset_type in ("shirt","pants"):
        template = Image.open(f"src/cache/templates/{asset_type}.png")
    else:
        return False

    asset.paste(template, (0, 0), mask=template)
    res_name = "src/cache/STRIP-"+sha256(str(uuid.uuid4()).encode("utf-8")).hexdigest()+".png"
    asset.save(res_name)

    # Will use the file for something later
    os.remove(file_name)
    return {"type": asset_bytes["type"], "file": res_name}


# TODO: make uploader a global
def republish_asset(
    asset_id: int,
    uploader,
    remove_watermark=True,
) -> Any:
    """
    Republishes an asset

    :param asset_id:
    :param uploader:
    :param bool remove_watermark:

    """

    if remove_watermark:
        asset = stripAssetWatermark(asset_id=asset_id)
        if not asset:
            # most likely a  tshirt
            return republish_asset(asset_id=asset_id, remove_watermark=False, uploader=uploader)
        asset_path = asset["file"]

    else:

        asset = fetchAssetBytes(asset_id)
        asset_path = "src/cache/" + str(sha256(str(asset_id).encode("utf-8")).hexdigest()) + ".png"

        with open(asset_path, "wb") as file:
            file.write(asset["bytes"])

    asset_attempts = 0
    while True:
        asset_details = getAssetDetails(asset_id)
        asset_attempts += 1

        if asset_details:
            break
        elif asset_attempts > 5:
            raise AssetDetailsNotFound("Unable to find asset details")
        else:
            time.sleep(1.5)

    if asset["type"].lower() == "shirt graphic" or asset["type"] == "TShirt":
        asset_type = "TShirt"
    elif asset:
        asset_type = asset["type"].lower().capitalize()

    if not asset_type.lower() in ("shirt", "pants", "tshirt"):
        raise InvalidAssetType("Asset Type provided is not valid")

    republish = uploader.uploadGroupAsset(
        group_id=cfg_file["group"]["group_id"],
        asset_type=asset_type,
        asset_name=asset_details["name"],
        bin_file=open(asset_path, "rb"),
    )

    os.remove(asset_path)

    return republish


def get_fp_assets(
    subcategory: str,
    limit: int = 120,
    cursor: Optional[str] = None,
    keyword: Optional[str] = None
) -> Dict:

    """
    Gets frontpage/popular items assets

    :param limit:
    :param subcategory: The subcategory(e.g. ClassicShirts,ClassicPants)
    :param Optional cursor:
    :param Optional keyword:

    :return: Dict

    """
    search_req = requests.get(
        url="https://catalog.roblox.com/v1/search/items",
        params={
            "category": "Clothing",
            "limit": limit,
            "salesTypeFilter": 1,
            "subcategory": subcategory,
            "cursor": cursor,
            "keyword": keyword
        },
    )

    if search_req.ok:
        return search_req.json()

    elif search_req.status_code == 429:
        logger.error("Ratelimited while attempting to scrape fp assets... Retrying..")
        time.sleep(cfg_file["other"]["ratelimit_wait_time"] or 4)
        return get_fp_assets(subcategory=subcategory, limit=limit,  cusror=cursor, keyword=keyword)

    else:
        logger.error(f"Asset scrape error:\nRequest status code: {search_req.status_code}\nText response: {search_req.text}\nHeaders:\n{search_req.headers}")
        raise Exception(search_req.text)

