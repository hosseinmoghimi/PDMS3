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
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
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
    
