from django import template
from django.http.request import bytes_to_text
register = template.Library()
from utility.persian import PersianCalendar

@register.filter
def to_persian_datetime(value):
    try:    
        a=PersianCalendar().from_gregorian(value)        
        return f'<span title="{value.strftime("%Y/%m/%d %H:%M:%S") }">{str(a)}</span>'
    except:
        return None

@register.filter
def to_week_day_name(date):
    a="_"
    aa=['شنبه'
    ,'یکشنبه'
    ,'دوشنبه'
    ,'سه شنبه'
    ,'چهارشنبه'
    ,'پنج شنبه'
    ,'جمعه']
    try:
        b=(date.weekday()+3)%7
        a=aa[b]
        # return str(b)
    except:
        pass
    return a

@register.filter
def to_persian_date(value):
    try:    
        a=PersianCalendar().from_gregorian(value)[:10]        
        return f'<span title="{value.strftime("%Y/%m/%d") }">{str(a)}</span>'
    except:
        return None