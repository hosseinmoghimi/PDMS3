from django.shortcuts import reverse
from django import template
register = template.Library()
from core.settings import ADMIN_URL
@register.filter
def get_edit_url(self):
    return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/change/"
@register.filter
def get_edit_btn(self):
    return f"""
            <a title="ویرایش" href="{get_edit_url(self)}">
                <span class="material-icons">
                    edit
                </sapn>
            </a>
        """
@register.filter
def get_absolute_url(self):
    return reverse(self.app_name+":"+self.class_name,kwargs={'pk':self.pk}) 
    # return f"{SITE_URL}{self.app_name}/{self.class_name}/{self.pk}/"
