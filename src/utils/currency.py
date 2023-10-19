def isFloatOrDigit(input):
    try:
        float(input)
        return True
    except:
        return False


def robux_price(robux: int, rate: int) -> float:
    """ 
    Converts the amount of robux to standard currency using the rate given
    The answer is given in to 2 decimal places
    
    :param int robux:
    :param int rate:

    :return: float
    """
    
    if float(rate).is_integer():
        rate = int(rate)
    else:
        rate = float(rate)

    conversion = (robux / 1000) * rate

    return float("{:.2f}".format(conversion))
