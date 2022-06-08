from django.db import models
from django.shortcuts import reverse
from pdms.settings import ADMIN_URL
from django.utils.translation import gettext as _

class LinkHelper():
    def get_absolute_url(self):
        return reverse(f"{self.app_name}:{self.class_name}",kwargs={'pk':self.pk})
    def get_edit_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/change/"
    def get_delete_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/delete/"