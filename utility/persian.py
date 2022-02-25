from django.utils import timezone
import datetime
from khayyam import *
PERSIAN_MONTH_NAMES=[
'فروردین',
'اردیبهشت',
'خرداد',
'تیر',
'مرداد',
'شهریور',
'مهر',
'آبان',
'آذر',
 'دی',
 'بهمن',
 'اسفند'
]
def days_in_month(year,month,day=1):
    nn=JalaliDate(year=year,month=month,day=day)
    return nn.daysinmonth


class PersianCalendar:
    def tag(self,value):
        a=self.from_gregorian(value)
        return f'<span title="{value.strftime("%Y/%m/%d %H:%M:%S") }">{str(a)}</span>'
    def to_gregorian(self,persian_date_input):
        if persian_date_input is None or persian_date_input=="" :
            return None
        return self.parse(persian_date_input).date
        
    def __init__(self,date=None):
        if date is None:
            from django.utils import timezone as timezone1
            self.date=timezone1.now()
            self.persian_date=self.from_gregorian(greg_date_time=self.date)
        if date is not None:
            self.date=date
            self.persian_date=self.from_gregorian(greg_date_time=self.date)
    
    def parse(self,value,add_time_zone=False):
        if value=="":
            return None
        shamsi_date_time=value

        year_=int(shamsi_date_time[0:4])
        month_=int(shamsi_date_time[5:7])
        day_=int(shamsi_date_time[8:10])
        padding=shamsi_date_time.find(':')
        if not padding==-1:
            padding-=2
            hour_=int(shamsi_date_time[padding:padding+2])
            
            padding+=3
            min_=int(shamsi_date_time[padding:padding+2])
            padding+=3
            sec_=int(shamsi_date_time[padding:padding+2])
           
        else:
            hour_=0
            min_=0
            sec_=0
        self.persian_date = JalaliDatetime(year_, month_, day_, hour_, min_, sec_, 0)
        delta=datetime.timedelta(hours=-3,minutes=-30)
        delta=datetime.timedelta(hours=0,minutes=0)
        self.date=self.persian_date.todatetime()+delta
        
        return self
    def from_gregorian(self,greg_date_time,add_time_zone=True):
        if greg_date_time is None:
            return None
        year_=greg_date_time.year
        month_=greg_date_time.month
        day_=greg_date_time.day
        try:
            hour_=greg_date_time.hour
        except:
            hour_=0
        try:
            min_=greg_date_time.minute
        except:
            min_=0
        try:
            sec_=greg_date_time.second
        except:
            sec_=0
            
        sss=TehranTimezone()
        delta=datetime.timedelta(hours=3,minutes=30)
        a=JalaliDatetime(datetime.datetime(year_, month_, day_, hour_, min_, sec_, 0, TehranTimezone())+delta)
        return a.strftime("%Y/%m/%d %H:%M:%S")
    def from_gregorian_date(self,greg_date):
        return JalaliDate.to_jalali(greg_date).strftime("%Y/%m/%d") 
