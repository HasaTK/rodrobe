class InvalidCredentialsError(Exception):
    """ 
    Raised if credentials provided are invalid 
    """
    
    pass 

class InvalidConfigException(Exception):
    """ 
    Raised if the config requested does not exist
    """

    pass


class InvalidWebhookException(Exception):
    """ 
    Raised if webhook provided is invalid
    """

    pass 

class AccountNotInGroup(Exception):
    """ 
    Raised if account is not in the specified group ID
    """

    pass 


class LowRankException(Exception):
    """ 
    Raised if the rank specified is too low
    """

    pass

class InvalidAssetId(Exception):
    """ 
    Raised if the asset ID provided is invalid
    """

    pass

class InvalidAssetType(Exception):

    """ 
    Raised if the asset type provided is invalid
    """

    pass

class AssetDetailsNotFound(Exception):
    """ 
    Raised if the details of an asset are not found
    """ 

    pass


class InvalidGroupID(Exception):
    """ 
    Raised if group ID provided is invalid
    """

    pass