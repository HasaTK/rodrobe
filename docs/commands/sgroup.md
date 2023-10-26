# sgroup Command

### Aliases: sg, stealgroup, rg, republishgroup, repgroup, repg

This command reuploads as many assets as the uploader account can from the given group id.
It uses the `item_price` and `tshirt_price` from the config file

## Arguments
<...> = Required argument

[...] Optional argument

- <group_id> - The ID of the group
- [remove_watermark] - True/False. By default this is true. If the asset is a T-Shirt then the
 program will leave the asset unchanged.

## Example Usage:
    !sgroup 3127877

OR

    !sgroup 3127877 false
