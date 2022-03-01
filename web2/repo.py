import json
from pdms.server_settings import COM_SERVER_IS_CONNECTED
from web2.enums import FeederComponentNameEnum
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
        # address=kwargs['address'] if 'address' in kwargs else COM_SERVER_START_ADDRESS_FOR_READING
        # count=kwargs['count'] if 'count' in kwargs else COM_SERVER_COUNT_OF_REGISTERS_FOR_READING
        values=None
        TEST=False
        if not COM_SERVER_IS_CONNECTED:
            return
        com_server_datas=ComServerDataBlock.objects.filter(com_server=com_server)
        leo_modbus=LeoModbus(request=self.request)
        leo_modbus.connect(host=com_server.ip1,port=com_server.port1)
        if not leo_modbus.is_open():
            return
        for com_server_data in com_server_datas:
            start_address=com_server_data.start_address
            count=com_server_data.count
            register=start_address
            if com_server_data.code_name==ComServerOperationCodeEnum.READ_HOLDING_REGISTERS:
                values=leo_modbus.read_holding_registers(start_address,count)
                if values is None:
                    return
                for value in values:
                    
                    feeder=Feeder.objects.filter(com_server=com_server).filter(
                        Q(register_ct_i_a=register) |
                        Q(register_ct_i_b=register) |
                        Q(register_ct_i_c=register) |

                        Q(register_vt_v_a=register) |
                        Q(register_vt_v_b=register) |
                        Q(register_vt_v_c=register) |
                        
                        Q(register_vt_v_ab=register) |
                        Q(register_vt_v_ac=register) |
                        Q(register_vt_v_bc=register) |
                        
                        Q(register_q=register) |
                        Q(register_p=register) |
                        Q(register_s=register) 

                    ).first()
                    if feeder is not None:
                        ctd=AnalogComponent()

                        ctd.feeder=feeder
                        if feeder.register_ct_i_a==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_I_A
                        if feeder.register_ct_i_b==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_I_B
                        if feeder.register_ct_i_c==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_I_C
                        
                        if feeder.register_vt_v_a==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_V_A
                        if feeder.register_vt_v_b==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_V_B
                        if feeder.register_vt_v_c==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_V_C
                        
                        if feeder.register_vt_v_ab==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_V_AB
                        if feeder.register_vt_v_ac==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_V_AC
                        if feeder.register_vt_v_bc==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_V_BC
                        
                        if feeder.register_q==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_P
                        if feeder.register_p==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_Q
                        if feeder.register_s==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_S

                        ctd.origin_value=value
                        ctd.status=InputOutputStatusEnum.SUCCESSFULL
                        ctd.save()
                    register+=1
            if com_server_data.code_name==ComServerOperationCodeEnum.READ_COILS:
                values=leo_modbus.read_coils(start_address,count)
                register=start_address
                
                values= [True, False, False, False, False]
                if values is not None:
                    for value in values:
                        feeder=Feeder.objects.filter(com_server=com_server).filter(
                            
                            Q(register_cb_open=register) |
                            Q(register_cb_close=register) |
                            Q(register_cb_test=register) |
                            Q(register_cb_trip=register) 

                        ).first()
                        if feeder is not None:
                            cb=BinaryComponent()

                            cb.feeder=feeder
                            if feeder.register_cb_open==register:
                                cb.name=FeederComponentNameEnum.REGISTER_CB_OPEN
                            if feeder.register_cb_close==register:
                                cb.name=FeederComponentNameEnum.REGISTER_CB_CLOSE
                            if feeder.register_cb_test==register:
                                cb.name=FeederComponentNameEnum.REGISTER_CB_TEST
                            if feeder.register_cb_trip==register:
                                cb.name=FeederComponentNameEnum.REGISTER_CB_TRIP

                            cb.origin_value=value
                            if feeder.register_cb_open==register:
                                cb.origin_value=1
                            cb.status=InputOutputStatusEnum.SUCCESSFULL
                            cb.save()
                        register+=1
            com_server_data.save()
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
        self.objects=Feeder.objects.all().order_by('priority')
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for))
        if 'bus_id' in kwargs:
            bus_id=kwargs['bus_id']
            objects=objects.filter(Q(bus_id=bus_id))
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
    
