from django.db import models
from django.forms import CharField
from core.models import _,LinkHelper,reverse
from web.apps import APP_NAME



class Feeder(models.Model,LinkHelper):
    bus=models.ForeignKey("bus", verbose_name=_("bus"), on_delete=models.CASCADE)
    com_server=models.ForeignKey("comserver", verbose_name=_("com_server"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=100)
    
    class_name="feeder"
    app_name=APP_NAME
    def com_server_set(self):
        return ComServer.objects.filter(pk=self.com_server.id)

    class Meta:
        verbose_name = _("Feeder")
        verbose_name_plural = _("Feeders")

    def __str__(self):
        return self.name 


class Bus(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=100)
    
    class_name="bus"
    app_name=APP_NAME
    

    class Meta:
        verbose_name = _("Bus")
        verbose_name_plural = _("Buses")

    def __str__(self):
        return self.name 


class ComServer(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=100)
    
    class_name="comserver"
    app_name=APP_NAME
    

    class Meta:
        verbose_name = _("ComServer")
        verbose_name_plural = _("ComServers")

    def __str__(self):
        return self.name 


class ComServerDataBlock(models.Model,LinkHelper):
    com_server=models.ForeignKey("comserver", verbose_name=_("com_server"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=100)
    
    class_name="comserverdatablock"
    app_name=APP_NAME
    

    class Meta:
        verbose_name = _("ComServerDataBlock")
        verbose_name_plural = _("ComServerDataBlock")

    def __str__(self):
        return self.name 