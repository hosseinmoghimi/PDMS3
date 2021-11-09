from django.contrib import admin
from web.models import AnalogInput, BinaryInput, BinaryOutput, Employee, Feeder,ComServer,Area,Permission,Bus
admin.site.register(Feeder)
admin.site.register(ComServer)
admin.site.register(BinaryInput)
admin.site.register(BinaryOutput)
admin.site.register(AnalogInput)
admin.site.register(Area)
admin.site.register(Bus)
admin.site.register(Employee)
admin.site.register(Permission)