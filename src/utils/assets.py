
import requests
import re,os
import uuid

from src.utils      import log
from hashlib        import sha256

from PIL            import Image
from src.exceptions import InvalidAssetId

from typing import Optional

def fetchAssetBytes(asset_id: int):
    """ 
    Fetches the asset bytes

    :param int asset_id:
    :return: bytes

    """    

    asset_xml = requests.get(f"https://assetdelivery.roblox.com/v1/asset?id={asset_id}")

    if asset_xml.ok:
        rId = (re.findall(r'<url>(.+?)(?=</url>)',asset_xml.text)[0]).replace("http://www.roblox.com/asset/?id=","")
        rType = re.findall(r'<string name="Name">(.+?)(?=</string>)', asset_xml.text)[0]

        assetData = requests.get(f"https://assetdelivery.roblox.com/v1/assetId/{rId}")
        fbytes = requests.get(assetData.json()["location"]).content
        return {"type":rType,"bytes":fbytes}
    else:
        raise InvalidAssetId("Asset ID is invalid")


def getAssetDetails(asset_id: int, csrf_token: Optional[str] = "roblox"):
    """ 
    Fetches the details of the asset
    
    :param int asset_id:
    :param Optional csrf_token:

    :return: details
    """

    details = requests.post(
        "https://catalog.roblox.com/v1/catalog/items/details",
        json={"items":[{"id":asset_id,"itemType":"asset"}]},
        headers={"content-type":"application/json","x-csrf-token":csrf_token}
    )

    if details.status_code == 403 and "Token Validation Failed" in details.text:
        return getAssetDetails(asset_id, details.headers["x-csrf-token"])

    elif details.ok:
        return details.json()['data'][0]
    
    return None


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
        log.error("Asset type not supported",__name__)
        return 
    
    
    asset.paste(template, (0,0), mask = template)
    res_name = "src/cache/STRIP-"+sha256(str(uuid.uuid4()).encode("utf-8")).hexdigest()+".png"
    asset.save(res_name)
    
    # Will use the file for something later
    os.remove(file_name)
    return res_name