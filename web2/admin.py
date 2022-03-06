from django.contrib import admin
from .models import BinaryComponent, ComServerDataBlock, AnalogComponent, Employee, Feeder,ComServer,Area, FeederComponent,Permission,Bus
admin.site.register(Feeder)
admin.site.register(ComServer)
admin.site.register(Area)
admin.site.register(ComServerDataBlock)
admin.site.register(FeederComponent)
admin.site.register(AnalogComponent)
admin.site.register(BinaryComponent)
admin.site.register(Bus)
admin.site.register(Employee)
admin.site.register(Permission)