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