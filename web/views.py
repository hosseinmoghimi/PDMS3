from django.shortcuts import render
from web.apps import APP_NAME
from django.views import View
from core.views import CoreContext
from web.repo import FeederRepo,BusRepo,ComServerRepo
TEMPLATE_ROOT="web/"
LAYOUT_PARENT="dashboard-en/layout.html"

def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        buses=BusRepo(request=request).list(*args, **kwargs)
        context['buses']=buses
        return render(request,TEMPLATE_ROOT+"index.html",context)

class BusView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        bus=BusRepo(request=request).bus(*args, **kwargs)
        context['bus']=bus
        feeders=FeederRepo(request=request).list(bus_id=bus.id)
        context['feeders']=feeders
        return render(request,TEMPLATE_ROOT+"bus.html",context)

class ComServerView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        com_server=ComServerRepo(request=request).com_server(*args, **kwargs)
        context['com_server']=com_server
        return render(request,TEMPLATE_ROOT+"com-server.html",context)

class FeederView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        feeder=FeederRepo(request=request).feeder(*args, **kwargs)
        context['feeder']=feeder
        com_servers=feeder.com_server_set().all()
        context['com_servers']=com_servers
        return render(request,TEMPLATE_ROOT+"feeder.html",context)
