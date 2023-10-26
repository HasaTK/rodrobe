# Steal Command

### Aliases: republish, repub, rp, rb

The steal command re-uploads the selected asset to your group and puts it on sale. 
The program will use either the `tshirt_price`  or the `item_price` config depending on wether
the item is a tshirt or a shirt/pant.


## Arguments
<...> = Required argument

[...] Optional argument

 - <asset_id> - The id of the asset you want to steal
 - [remove_watermark] - True/False. By default this is true. If the asset is a T-Shirt then the
 program will leave the asset unchanged.

## Example Usage:
    !steal 398633584
OR

    !steal 398633584 false
