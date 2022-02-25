from core.errors import LEO_ERRORS
from django import template
register = template.Library()
from utility.currency import to_price as to_price_origin
from utility.num import to_horuf as to_horuf_num,to_tartib as to_tartib_
RIAL="ریال"
@register.filter
def to_price(value):
    return to_price_origin(value=value)

@register.filter
def to_price_rial(value):
    return to_price_x10(value=value*10)+" "+RIAL


@register.filter
def to_price_x10(value):
    return to_price_pure(value=value*10)


@register.filter
def to_horuf(value):
    return to_horuf_num(value)




@register.filter
def to_horuf_x10(value):
    return to_horuf_num(value*10)




@register.filter
def to_tartib(value):
    return to_tartib_(value)




@register.filter
def to_price_pure(value):
    """converts int to string"""  
    try:
        sign=''
        if value<0:
            value=0-value
            sign='- '
        a=separate(value)
        return sign+a
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
