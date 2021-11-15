from pdms.server_settings import COM_SERVER_IS_CONNECTED
from .modbus import LeoModbus
from django.http import request
from .models import *
from .constants import *
from authentication.repo import ProfileRepo
from django.db.models import Q
from authentication.repo import ProfileRepo

class ComServerRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.objects=ComServer.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for))
        return objects
        
    def read(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".view_comserver"):
            return
        com_server=self.com_server(*args, **kwargs)
        if com_server is None:
            return
        address=kwargs['address'] if 'address' in kwargs else COM_SERVER_START_ADDRESS_FOR_READING
        count=kwargs['count'] if 'count' in kwargs else COM_SERVER_COUNT_OF_REGISTERS_FOR_READING
        values=None
        TEST=False
        if COM_SERVER_IS_CONNECTED:
            leo_modbus=LeoModbus(request=self.request)
            leo_modbus.connect(host=com_server.ip1,port=com_server.port1)
            values=leo_modbus.read_holding_registers(address=address,count=count)
        register=address
        if values is None:
            import random
            for i in range(count):
                ai=AnalogInput()
                ai.register=register
                ai.com_server=com_server
                ai.status=InputOutputStatusEnum.INVALID
                ai.status=InputOutputStatusEnum.SUCCESSFULL
                ai.origin_value=str(random.randint(310,330))
                # print(ai.origin_value)
                # print(10*"#@#$")
                ai.save()
                register+=1
            return None
        for value in values:
            ai=AnalogInput()
            ai.register=register
            ai.com_server=com_server
            ai.origin_value=value
            ai.status=InputOutputStatusEnum.SUCCESSFULL
            ai.save()
            register+=1
        return values
        
    def com_server(self,*args, **kwargs):
        pk=0
        if 'com_server_id' in kwargs:
            pk=kwargs['com_server_id']
        elif 'id' in kwargs:
            pk=kwargs['id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'title' in kwargs:
            return self.objects.filter(title=kwargs['title']).first()
        return self.objects.filter(pk=pk).first()
    

class AreaRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=Area.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for))
        return objects
    def area(self,*args, **kwargs):
        pk=0
        if 'area_id' in kwargs:
            pk=kwargs['area_id']
        elif 'id' in kwargs:
            pk=kwargs['id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'title' in kwargs:
            return self.objects.filter(title=kwargs['title']).first()
        return self.objects.filter(pk=pk).first()
    


class BusRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=Bus.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for))
        return objects
    def bus(self,*args, **kwargs):
        pk=0
        if 'bus_id' in kwargs:
            pk=kwargs['bus_id']
        elif 'id' in kwargs:
            pk=kwargs['id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'title' in kwargs:
            return self.objects.filter(title=kwargs['title']).first()
        return self.objects.filter(pk=pk).first()
    


class FeederRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=Feeder.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for))
        return objects
    def feeder(self,*args, **kwargs):
        pk=0
        if 'feeder_id' in kwargs:
            pk=kwargs['feeder_id']
        elif 'id' in kwargs:
            pk=kwargs['id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'title' in kwargs:
            return self.objects.filter(title=kwargs['title']).first()
        return self.objects.filter(pk=pk).first()
    
