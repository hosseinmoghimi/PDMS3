from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import *
from core.constants import SUCCEED,FAILED
from .repo import *
from .forms import *


class ComServerApi(APIView):
    def read_com_server(self,request,*args, **kwargs):
        user=request.user
        context={}
        context['result']=FAILED

        if request.method=='POST':
            read_com_server_form=ReadComServerForm(request.POST)
            if read_com_server_form.is_valid():
                com_server_id=read_com_server_form.cleaned_data['com_server_id']
                address=read_com_server_form.cleaned_data['address']
                count=read_com_server_form.cleaned_data['count']
                values=ComServerRepo(request=request).read(address=address,count=count,com_server_id=com_server_id)
                if values is not None:
                    context['values']=values
                    context['result']=SUCCEED
        return JsonResponse(context)

class FeederApi(APIView):
    def get_feeder(self,request,*args, **kwargs):
        user=request.user
        context={}
        context['result']=FAILED
        if request.method=='POST':
            get_feeder_form=GetFeederForm(request.POST)
            if get_feeder_form.is_valid():
                feeder_id=get_feeder_form.cleaned_data['feeder_id']
                feeder=FeederRepo(request=request).feeder(feeder_id=feeder_id)
                # ComServerRepo(request=request).read(address=feeder.address,count=25,com_server_id=feeder.com_server_id)
                address=5
                count=9
                com_server_id=feeder.com_server.pk
                # vvvv=ComServerRepo(request=request).read(com_server_id=com_server_id,address=address,count=count)
                # print("com_server_id")
                # print(com_server_id)

                # print("address")
                # print(address)
                # print("port:")
                # print(count)
                # print(vvvv)

                # print(100*"$%$#$")
                if feeder is not None:
                    # feeder.update_data()
                    context['feeder']=FeederFullSerializer(feeder).data
                    values=feeder.get_last_values(10)
                    context[FeederComponentNameEnum.REGISTER_I_A]=list(i.value() for i in values[FeederComponentNameEnum.REGISTER_I_A])
                    context[FeederComponentNameEnum.REGISTER_I_B]=list(i.value() for i in values[FeederComponentNameEnum.REGISTER_I_B])
                    context[FeederComponentNameEnum.REGISTER_I_C]=list(i.value() for i in values[FeederComponentNameEnum.REGISTER_I_C])
                    context[FeederComponentNameEnum.REGISTER_V_A]=list(i.value() for i in values[FeederComponentNameEnum.REGISTER_V_A])
                    context[FeederComponentNameEnum.REGISTER_V_B]=list(i.value() for i in values[FeederComponentNameEnum.REGISTER_V_B])
                    context[FeederComponentNameEnum.REGISTER_V_C]=list(i.value() for i in values[FeederComponentNameEnum.REGISTER_V_C])
                    context['result']=SUCCEED
        return JsonResponse(context)

class BasicApi(APIView):
    def add_com_server(self,request,*args, **kwargs):
        context={}
        context['result']=SUCCEED
        return JsonResponse(context)
    def circuit_breaker_toggle(self,request,*args, **kwargs):
        user=request.user
        context={}
        if request.method=='POST':
            add_input_command_form=ToggleCircuitBreakerForm(request.POST)
            if add_input_command_form.is_valid():
                cb_id=add_input_command_form.cleaned_data['cb_id']
                command=add_input_command_form.cleaned_data['command']
                cb=CircuitBreakerRepo(user=request.user,request=request).circuit_breaker_toggle(pk=cb_id,user=request.user)
                context['circuit_breaker']=CircuitBreakerSerializer(cb).data
                context['circuit_breakers']=CircuitBreakerSerializer(cb.feeder.circuitbreakers(),many=True).data
                context['result']=CoreConstants.SUCCEED
        return JsonResponse(context)

    def circuit_breaker_read(self,request,*args, **kwargs):
        user=request.user
        context={}
        if request.method=='POST':
            read_circuit_breaker_form=ReadCircuitBreakerForm(request.POST)
            if read_circuit_breaker_form.is_valid():
                cb_id=read_circuit_breaker_form.cleaned_data['cb_id']
                cb=CircuitBreakerRepo(user=request.user,request=request).circuit_breaker(pk=cb_id)
                value=cb.get_value(request=request)
                context['value']=value
                print("value: "+str(value))
                context['circuit_breaker']=CircuitBreakerSerializer(cb).data
                context['circuit_breakers']=CircuitBreakerSerializer(cb.feeder.circuitbreakers(),many=True).data
                context['result']=CoreConstants.SUCCEED
        return JsonResponse(context)
    def get_bus_data(self,request,*args, **kwargs):
        user=request.user
        context={}
        if request.method=='POST':
            get_bus_data_form=GetBusDataForm(request.POST)
            if get_bus_data_form.is_valid():
                bus_id=get_bus_data_form.cleaned_data['bus_id']
                feeders=FeederRepo(user=request.user).list(bus_id=bus_id)
                bus=BusRepo(user=request.user).bus(pk=bus_id)
                context['feeders']=FeederSerializerForChart(feeders,many=True).data
                context['bus']=BusSerializer(bus).data
                context['result']=SUCCEED
        return JsonResponse(context)
    def get_feeder_data(self,request,*args, **kwargs):
        user=request.user
        context={}
        level=1
        feeder=None
        context['result']=FAILED
        if request.method=='POST':
            level=2
            
            get_feeder_data_form=GetFeederDataForm(request.POST)
            if get_feeder_data_form.is_valid():
                level=3
                feeder_id=get_feeder_data_form.cleaned_data['feeder_id']
                FeederRepo(user=request.user).create_sample_data(feeder_id=feeder_id)
                feeder=FeederRepo(user=request.user).feeder(feeder_id)
                feeder.circuit_breaker.get_value(request)
        elif request.method=='GET' and 'pk' in kwargs:
            level=4
            feeder_id=kwargs['pk']
            feeder=FeederRepo(user=request.user).feeder(feeder_id)
        if feeder is not None:
            level=5
            context['feeder']=FeederSerializerForChart(feeder).data
            context['value_a_list']=list(ai.value for ai in feeder.current_transformer.value_a_list())
            context['value_b_list']=list(ai.value for ai in feeder.current_transformer.value_b_list())
            context['value_c_list']=list(ai.value for ai in feeder.current_transformer.value_c_list())

            context['result']=SUCCEED
        context['level']=level
        return JsonResponse(context)


    def get_analog_data(self,request,*args, **kwargs):
        user=request.user
        context={}
        if request.method=='POST':
            get_analog_data_form=GetAnalogDataForm(request.POST)
            if get_analog_data_form.is_valid():
                host=get_analog_data_form.cleaned_data['host']
                port=get_analog_data_form.cleaned_data['port']
                address=get_analog_data_form.cleaned_data['address']
                count=get_analog_data_form.cleaned_data['count']
                from .modbus import LeoModbus
                leo_modbus=LeoModbus(user=request.user)
                leo_modbus.connect(host=host,port=port)
                data=leo_modbus.read_holding_registers(address=address,count=count)
                print(data)
                context['data']=data
                context['result']=SUCCEED
        return JsonResponse(context)