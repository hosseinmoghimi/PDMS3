from django.contrib import admin

from web.models import Bus, ComServerDataBlock, Feeder,ComServer


admin.site.register(ComServer)
admin.site.register(Feeder)
admin.site.register(Bus)
admin.site.register(ComServerDataBlock)