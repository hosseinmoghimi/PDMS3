from core.errors import LEO_ERRORS
from core.constants import CURRENCY


def to_price(value,unit=CURRENCY):
    """converts int to string"""  
    try:
        value=int(value)
        sign=''
        if value<0:
            value=0-value
            sign='- '
        a=separate(value)
        return sign+a+' '+unit
    except:
        # return LEO_ERRORS.error_to_price_template_tag
        return ""


def separate(price):
    
    try:
        price=int(price)
    except:
        return None
    
    if price<1000:
        return str(price)
    else:
        return separate(price/1000)+','+str(price)[-3:]
