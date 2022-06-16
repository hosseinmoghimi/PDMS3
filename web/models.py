from web.enums import *
from django.db import models
from django.db.models import Q
from core.models import _,LinkHelper,reverse
from web.apps import APP_NAME
from web.constants import *



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
    ip1=models.CharField(_("ip1"),default=COM_SERVER_DEFAULT_IP, max_length=50)
    port1=models.CharField(_("port1"),default=str(COM_SERVER_DEFAULT_PORT), max_length=50)
    ip2=models.CharField(_("ip2"),default="192.168.2.254", max_length=50)
    port2=models.CharField(_("port2"),default="8080", max_length=50)
    username=models.CharField(_("username"),default=COM_SERVER_DEFAULT_USER_NAME, max_length=50)
    password=models.CharField(_("password"),default=COM_SERVER_DEFAULT_PASSWORD, max_length=50)
    redundancy=models.CharField(_("redundancy"),choices=ComServerRedundancyEnum.choices,default=ComServerRedundancyEnum.HOT, max_length=50)
    interval=models.IntegerField(_("interval"), default=5000)
    color="primary"
    reading=False
    class_name="comserver"
    app_name=APP_NAME
    

    class Meta:
        verbose_name = _("ComServer")
        verbose_name_plural = _("ComServers")

    def __str__(self):
        return self.name 

    def read(self,request,*args, **kwargs):
        com_server=self
        if com_server is None:
            return
        com_server_datas=ComServerDataBlock.objects.filter(com_server_id=com_server.id)
        from web.modbus import LeoModbus
        leo_modbus=LeoModbus(request=request)
        leo_modbus.connect(host=com_server.ip1,port=com_server.port1)
        values=[]
        if not leo_modbus.is_open():
            return
        for com_server_data in com_server_datas:
            start_address=com_server_data.start
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
                            feeder.i_a=value
                        if feeder.register_ct_i_b==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_I_B
                            feeder.i_b=value
                        if feeder.register_ct_i_c==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_I_C
                            feeder.i_c=value
                        
                        if feeder.register_vt_v_a==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_V_A
                            feeder.v_a=value
                        if feeder.register_vt_v_b==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_V_B
                            feeder.v_b=value
                        if feeder.register_vt_v_c==register:
                            ctd.name=FeederComponentNameEnum.REGISTER_V_C
                            feeder.v_c=value
                        
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

                        ctd.register=register
                        ctd.origin_value=value
                        ctd.status=InputOutputStatusEnum.SUCCESSFULL
                        ctd.save()
                        feeder.save()
                    register+=1
            if com_server_data.code_name==ComServerOperationCodeEnum.READ_COILS:
                values=leo_modbus.read_coils(start_address,count)
                register=start_address
                if values is None:
                    return
                    
                # values= [ True,False, False,False,  False]
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
                                feeder.circuit_breaker_status=CircuitBreakerStatusEnum.OPEN
                            if feeder.register_cb_close==register:
                                cb.name=FeederComponentNameEnum.REGISTER_CB_CLOSE
                                feeder.circuit_breaker_status=CircuitBreakerStatusEnum.CLOSE
                            if feeder.register_cb_test==register:
                                cb.name=FeederComponentNameEnum.REGISTER_CB_TEST
                                feeder.circuit_breaker_status=CircuitBreakerStatusEnum.TEST
                            if feeder.register_cb_trip==register:
                                cb.name=FeederComponentNameEnum.REGISTER_CB_TRIP
                                feeder.circuit_breaker_status=CircuitBreakerStatusEnum.TRIP
                            cb.origin_value=value
                            cb.register=register
                            cb.status=InputOutputStatusEnum.SUCCESSFULL
                            cb.save()
                            feeder.save()
                        register+=1
            com_server_data.save()
        return values


class ComServerDataBlock(models.Model,LinkHelper):
    com_server=models.ForeignKey("comserver", verbose_name=_("com_server"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=100)
    start=models.IntegerField(_("start"))
    count=models.IntegerField(_("count"))
    
    class_name="comserverdatablock"
    app_name=APP_NAME
    

    class Meta:
        verbose_name = _("ComServerDataBlock")
        verbose_name_plural = _("ComServerDataBlock")

    def __str__(self):
        return self.name 