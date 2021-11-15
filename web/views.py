import json
from django.http.response import Http404

from core.views import CoreContext
from web.serializers import AreaSerializer, BusSerializer, FeederFullSerializer, FeederSerializer, FeederSerializerForChart
from .apps import APP_NAME
from .forms import *
from .repo import AreaRepo, BusRepo,ComServerRepo, FeederRepo
from django.views import View
from django.shortcuts import redirect, render
TEMPLATE_ROOT = APP_NAME+"/"
LAYOUT_PARENT=""

def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context


class ComServerViews(View):
    def com_server(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        com_server=ComServerRepo(user=user).com_server(*args, **kwargs)
        context['com_server']=com_server
        return render(request,TEMPLATE_ROOT+'com-server.html',context)


class FeederViews(View):
    def feeder(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        feeder=FeederRepo(user=user).feeder(*args, **kwargs)
        context['feeder']=feeder
        feeder.update_circuit_breaker_status()
        feeder_s=json.dumps(FeederFullSerializer(feeder).data)
        context['feeder_s']=feeder_s
        return render(request,TEMPLATE_ROOT+'feeder.html',context)


class BasicViews(View):
    
    def add_input_command(self,request,*args, **kwargs):
        user=request.user
        if request.method=='POST':
            add_input_command_form=AddInputCommandForm(request.POST)
            if add_input_command_form.is_valid():
                input_id=add_input_command_form.cleaned_data['input_id']
                command=add_input_command_form.cleaned_data['command']
                BinaryCommandRepo(user=request.user).add_command(input_id)
                context=getContext(request)
                return render(request,TEMPLATE_ROOT+"index.html",context)

    def data(self,request):
        context=getContext(request)
        return render(request,TEMPLATE_ROOT+"data.html",context)
    
    def home(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        com_servers=ComServerRepo(user=user).list()
        feeders=FeederRepo(user=user).list()
        context['com_servers']=com_servers
        context['feeders']=feeders
        buses=BusRepo(request.user).list()
        context['buses']=buses
        feeders_s=json.dumps(FeederSerializer(feeders,many=True).data)
        context['feeders_s']=feeders_s
        areas=AreaRepo(user).list()
        areas_s=json.dumps(AreaSerializer(areas,many=True).data)
        context['areas_s']=areas_s
        return render(request,TEMPLATE_ROOT+'index.html',context)
    
    def node(self,request,pk,*args, **kwargs):
        user=request.user
        context=getContext(request)
        node=NodeRepo(user=user).node(pk=pk)
        context['node']=node
        return render(request,TEMPLATE_ROOT+'node.html',context)
    def logs(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        logs=LogRepo(user=user).list(*args, **kwargs)
        context['logs']=logs
        context['logs_s']=json.dumps(LogSerializer(logs,many=True).data)
        return render(request,TEMPLATE_ROOT+'logs.html',context)
    def log(self,request,pk,*args, **kwargs):
        user=request.user
        context=getContext(request)
        log=LogRepo(user=user).log(pk)
        context['log']=log
        context['log_s']=json.dumps(LogSerializer(log).data)
        return render(request,TEMPLATE_ROOT+'log.html',context)
    def demo(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        logs=LogRepo(user=user).list(*args, **kwargs)
        context['logs']=logs
        return render(request,TEMPLATE_ROOT+'demo.html',context)
    def bus(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        bus=BusRepo(user=user).bus(*args, **kwargs)
        context['bus']=bus
        return render(request,TEMPLATE_ROOT+'bus.html',context)
    def circuitbreaker(self,request,pk,*args, **kwargs):
        user=request.user
        context=getContext(request)
        bus=BusRepo(user=user).bus(pk)
        context['bus']=bus
        return render(request,TEMPLATE_ROOT+'circuit-breaker.html',context)
    def currenttransformer(self,request,pk,*args, **kwargs):
        user=request.user
        context=getContext(request)
        currenttransformer=CurrentTransformerRepo(user=user).currenttransformer(pk)
        context['currenttransformer']=currenttransformer
        return render(request,TEMPLATE_ROOT+'current-transformer.html',context)
    def voltagetransformer(self,request,pk,*args, **kwargs):
        user=request.user
        context=getContext(request)
        voltagetransformer=VoltageTransformerRepo(user=user).voltagetransformer(pk)
        context['voltagetransformer']=voltagetransformer
        return render(request,TEMPLATE_ROOT+'voltage-transformer.html',context)
  
    def area(self,request,pk,*args, **kwargs):
        user=request.user
        context=getContext(request)
        area=AreaRepo(user=user).area(pk)
        context['area']=area
        print(area)
        print(200*"*")
        return render(request,TEMPLATE_ROOT+'area.html',context)
    
    
    def monitoring(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        if 'bus_id' in kwargs:
            bus_id=kwargs['bus_id']        
            buses=BusRepo(user=user).list().filter(pk=bus_id)
            feeders=FeederRepo(request.user).list().filter(bus=buses.first())
        else:
            buses=BusRepo(user=user).list(*args, **kwargs)
            feeders=FeederRepo(request.user).list()
        context['buses']=buses
        buses_s=json.dumps(BusSerializer(buses,many=True).data)
        context['buses_s']=buses_s
        
        feeders_s=json.dumps(FeederSerializerForChart(feeders,many=True).data)
        context['feeders_s']=feeders_s
        context['feeders']=feeders
       
        context['bus_color']=buses.first().get_color()

        return render(request,TEMPLATE_ROOT+'monitoring.html',context)