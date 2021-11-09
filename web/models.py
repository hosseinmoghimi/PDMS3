from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _

from web.apps import APP_NAME

class Feeder(models.Model):
    name=models.CharField(_("name"), max_length=50)

    class_name="feeder"
    class Meta:
        verbose_name = _("Feeder")
        verbose_name_plural = _("Feeders")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})
