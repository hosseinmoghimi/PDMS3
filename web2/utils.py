from core.settings import ADMIN_URL,SITE_URL,MEDIA_URL
from .apps import APP_NAME
from django.shortcuts import reverse

def word_to_int(hex_str,length):
    max1=2**(length-1)
    print("max : "+str(max1))
    print("hex_str : "+str(hex_str))
    value = int(hex_str, length)
    value = int(hex_str)
    print("value : "+str(value))
    if value > max1:
        value =value-max1*2
    return value


class AdminUtility():
    def __init__(self,app_name,user):
        self.user=user
        self.app_name=app_name
    def get_link(self,child_class,class_title):
        app_name=self.app_name

        app_name=APP_NAME
        url=f'{ADMIN_URL}{app_name}/{child_class}/add/'
        return f"""
         <a class="btn btn-info rtl" target="_blank" href="{url}" title="افزودن {class_title}" >
                     <i class="material-icons">add_circle</i>
         <span >
         Add New  
         {class_title}
         </span>
                 </a>
        """
        
    
    def get_add_comserver(self):
        return self.get_link(child_class='comserver',class_title='ComServer')
    
    def get_add_bus(self):
        return self.get_link(child_class='bus',class_title='Bus')
    
    def get_add_feeder(self):
        return self.get_link(child_class='feeder',class_title='Feeder')
    