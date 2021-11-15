from django.db import models
from django.forms.fields import CharField
from django.shortcuts import reverse
from django.utils.translation import gettext as _

from pdms.server_settings import STATIC_URL
from .constants import *
from .enums import CircuitBreakerStatusEnum, ComServerRedundancyEnum, InputOutputStatusEnum,LogStatusEnum, VoltageLevelEnum
from .settings import ADMIN_URL
from .apps import APP_NAME

class Employee(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse("Employee_detail", kwargs={"pk": self.pk})



class ComServer(models.Model):
    name=models.CharField(_("name"), max_length=50)
    ip1=models.CharField(_("ip1"),default="192.168.1.254", max_length=50)
    port1=models.CharField(_("port1"),default=str(COM_SERVER_DEFAULT_PORT), max_length=50)
    ip2=models.CharField(_("ip2"),default="192.168.2.254", max_length=50)
    port2=models.CharField(_("port2"),default="8080", max_length=50)
    username=models.CharField(_("username"),default=COM_SERVER_DEFAULT_USER_NAME, max_length=50)
    password=models.CharField(_("password"),default=COM_SERVER_DEFAULT_PASSWORD, max_length=50)
    redundancy=models.CharField(_("redundancy"),choices=ComServerRedundancyEnum.choices,default=ComServerRedundancyEnum.HOT, max_length=50)
    
    class_name="comserver"
    
    class Meta:
        verbose_name = _("ComServer")
        verbose_name_plural = _("ComServers")


    def __str__(self):
        return self.name


    def get_edit_btn(self):
        return f"""
            <a target="_blank" title="Edit {self.name}" class="mx-2 btn btn-warning btn-link" href="{self.get_edit_url()}">
            <i class="material-icons">settings</i>
            </a>
        """


    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""



class Feeder(models.Model):
    name=models.CharField(_("name"), max_length=50)
    bus=models.ForeignKey("bus", verbose_name=_("bus"), on_delete=models.CASCADE)
    address=models.IntegerField(_("address"),default=0)
    com_server=models.ForeignKey("comserver", verbose_name=_("com_server"), on_delete=models.CASCADE)

    
    register_cb_open=models.IntegerField(_("register_cb_open"),default=REGISTER_CIRCUIT_BREAKER_OPEN)
    register_cb_close=models.IntegerField(_("register_cb_close"),default=REGISTER_CIRCUIT_BREAKER_CLOSE)
    register_cb_test=models.IntegerField(_("register_cb_test"),default=REGISTER_CIRCUIT_BREAKER_TEST)
    register_cb_trip=models.IntegerField(_("register_cb_trip"),default=REGISTER_CIRCUIT_BREAKER_TRIP)
    register_cb_servive=models.IntegerField(_("register_cb_trip"),default=REGISTER_CIRCUIT_BREAKER_SERVICE)
    register_cb_spare1=models.IntegerField(_("register_cb_spare1"),default=REGISTER_CIRCUIT_BREAKER_SPARE1)
    register_cb_spare2=models.IntegerField(_("register_cb_spare2"),default=REGISTER_CIRCUIT_BREAKER_SPARE2)

    register_ct_i_a=models.IntegerField(_("register I a"),default=REGISTER_CURRENT_TRANSFORMER_I_A)
    register_ct_i_b=models.IntegerField(_("register I b"),default=REGISTER_CURRENT_TRANSFORMER_I_B)
    register_ct_i_c=models.IntegerField(_("register I c"),default=REGISTER_CURRENT_TRANSFORMER_I_C)

    register_vt_v_a=models.IntegerField(_("register V a"),default=REGISTER_VOLTAGE_TRANSFORMER_V_A)
    register_vt_v_b=models.IntegerField(_("register V b"),default=REGISTER_VOLTAGE_TRANSFORMER_V_B)
    register_vt_v_c=models.IntegerField(_("register V c"),default=REGISTER_VOLTAGE_TRANSFORMER_V_C)

    register_vt_v_ab=models.IntegerField(_("register V ab"),default=REGISTER_VOLTAGE_TRANSFORMER_V_AB)
    register_vt_v_bc=models.IntegerField(_("register V bc"),default=REGISTER_VOLTAGE_TRANSFORMER_V_BC)
    register_vt_v_ac=models.IntegerField(_("register V ac"),default=REGISTER_VOLTAGE_TRANSFORMER_V_AC)

    register_q=models.IntegerField(_("register q"),default=REGISTER_Q)
    register_p=models.IntegerField(_("register p"),default=REGISTER_P)
    register_s=models.IntegerField(_("register s"),default=REGISTER_S)


    circuit_breaker_status=models.CharField(_("circuit_breaker_status"),choices=CircuitBreakerStatusEnum.choices, max_length=50)
    i_a=models.IntegerField(_("I a"),null=True,blank=True)
    i_b=models.IntegerField(_("I b"),null=True,blank=True)
    i_c=models.IntegerField(_("I c"),null=True,blank=True)
    class_name="feeder"

    def current_transformer(self):
        ct=CurrentTransformer()
        ct.feeder=self
        ct.update_data()
        return ct
    def update_circuit_breaker_status(self):
        status=CircuitBreakerStatusEnum.FAILED
        try:
            cb_open=BinaryInput.objects.filter(com_server=self.com_server).filter(register=self.address+self.register_cb_open).order_by('-date_added').first().value()
            cb_close=BinaryInput.objects.filter(com_server=self.com_server).filter(register=self.address+self.register_cb_close).order_by('-date_added').first().value()
            cb_test=BinaryInput.objects.filter(com_server=self.com_server).filter(register=self.address+self.register_cb_test).order_by('-date_added').first().value()
            cb_service=BinaryInput.objects.filter(com_server=self.com_server).filter(register=self.address+self.register_cb_service).order_by('-date_added').first().value()
            cb_spare1=BinaryInput.objects.filter(com_server=self.com_server).filter(register=self.address+self.register_cb_spare1).order_by('-date_added').first().value()
            cb_spare2=BinaryInput.objects.filter(com_server=self.com_server).filter(register=self.address+self.register_cb_spare2).order_by('-date_added').first().value()
            if cb_close:
                status= CircuitBreakerStatusEnum.CLOSE
            if cb_open:
                status= CircuitBreakerStatusEnum.OPEN
            if cb_test:
                status= CircuitBreakerStatusEnum.TESTING
        except:
            pass    
        import random
        
        status=CircuitBreakerStatusEnum.choices[random.randint(0,3)][0]
        self.circuit_breaker_status=status
        return status
            
    def update_data(self):
        self.update_circuit_breaker_status()
        self.i_a=AnalogInput.objects.filter(com_server=self.com_server).filter(register=self.address+self.register_ct_i_a).order_by('-date_added').first().value()
        self.i_b=AnalogInput.objects.filter(com_server=self.com_server).filter(register=self.address+self.register_ct_i_b).order_by('-date_added').first().value()
        self.i_c=AnalogInput.objects.filter(com_server=self.com_server).filter(register=self.address+self.register_ct_i_c).order_by('-date_added').first().value()
        self.save()
    def circuit_breaker_schematic(self):
        status=self.circuit_breaker_status
        if status==CircuitBreakerStatusEnum.OPEN and self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-open.png'
        if status==CircuitBreakerStatusEnum.CLOSE and self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-close.png'
        if status==CircuitBreakerStatusEnum.OPEN and not self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-open-bus-dead.png'
        if status==CircuitBreakerStatusEnum.CLOSE and not self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-close-bus-dead.png'

        if status==CircuitBreakerStatusEnum.FAILED :
            return f'{STATIC_URL}{APP_NAME}/img/cb-failed.png'
        if status==CircuitBreakerStatusEnum.TESTING:
            return f'{STATIC_URL}{APP_NAME}/img/cb-testing.png'
    def panel(self):
        # return ""
        components_panels=""
        components_panels+=f"""<div><img src="{self.circuit_breaker_schematic()}" width="100"></div>"""
        # components_panels+=self.current_transformer.panel()
        return f"""
            <div>
            
            {components_panels}
            <h3>
            <a href="{self.get_absolute_url()}">
            
            {self.name}
            </a>
            </h3>
            </div>
        """
    
    class Meta:
        verbose_name = _("Feeder")
        verbose_name_plural = _("Feeders")

    def __str__(self):
        return self.name
    def area(self):
        return self.bus.area
    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""




class Bus(models.Model):
    area=models.ForeignKey("area", verbose_name=_("area"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=50)
    tip=models.CharField(_("tip"),choices=VoltageLevelEnum.choices,null=True,blank=True, max_length=50)
    brand=models.CharField(_("brand"),null=True,blank=True, max_length=5000)
    model_name=models.CharField(_("model_name"),null=True,blank=True, max_length=5000)
    serial_no=models.CharField(_("serial_no"),null=True,blank=True, max_length=5000)
    description=models.CharField(_("description"),null=True,blank=True, max_length=5000)
    is_live=models.BooleanField(_("is live ?"),default=True)
    class_name="bus"
    def panel(self):
        return f"""
        <div>
        <a href="{self.get_absolute_url()}">
        {self.area.region}-{self.area.name} : {self.name} ({self.tip})
        </a>
        </div>
        """
    def save(self):
        self.child_class="bus"
        super(Bus,self).save()
    class Meta:
        verbose_name = 'Bus'
        verbose_name_plural = 'Buses'
    def get_absolute_url(self):
        return reverse(APP_NAME+":bus",kwargs={'pk':self.pk})
    def get_monitoring_url(self):
        return reverse(APP_NAME+":bus_monitoring",kwargs={'bus_id':self.pk})
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_monitoring_btn(self):
        return f"""
            <a title="Monitor {self.name}" class="btn btn-link btn-success" href="{self.get_monitoring_url()}">
            <i class="material-icons">
            settings
            </i>
            </a>
        """

    def get_color(self):
        if not self.is_live:
            return "#000"
        if self.tip==VoltageLevelEnum.MV:
            return "#1553A1"
        if self.tip==VoltageLevelEnum.LV:
            return "#D4233C"
        if self.tip==VoltageLevelEnum.HV:
            return "#083C72"


class Area(models.Model):
    region=models.CharField(_("region"), max_length=50)
    name=models.CharField(_("name"), max_length=50)
    gps=models.CharField(_("gps"),null=True,blank=True, max_length=50)
    def full_name(self):
        return self.name+" / " + self.region
    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return f'{self.region} => {self.name}'

    def get_absolute_url(self):
        return reverse(APP_NAME+":area", kwargs={"pk": self.pk})


class InputOutput(models.Model):
    com_server=models.ForeignKey("comserver", verbose_name=_("com_server"), on_delete=models.CASCADE)
    register=models.IntegerField(_("register"))
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    status=models.CharField(_("status"),choices=InputOutputStatusEnum.choices,default=InputOutputStatusEnum.DISCONNECTED, max_length=50)
    origin_value=models.CharField(_("origin_value"),null=True,blank=True, max_length=50)
    class Meta:
        verbose_name = _("InputOutput")
        verbose_name_plural = _("InputOutputs")

    def __str__(self):
        return f'{self.com_server.name} : {self.register}'


class Permission(models.Model):
    employee=models.ForeignKey("Employee", verbose_name=_("employee"),null=True,blank=True, on_delete=models.CASCADE)
    com_server=models.ForeignKey("comserver", verbose_name=_("comserver"), on_delete=models.CASCADE)
    register=models.IntegerField(_("register"))
    can_read=models.BooleanField(_("can_read"),default=False)
    can_write=models.BooleanField(_("can_write"),default=False)
    class Meta:
        
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'


class AnalogInput(InputOutput):
    def value(self):
        if self.origin_value is None:
            return None
        return int(self.origin_value) 
    
    class Meta:
        verbose_name = _("AI")
        verbose_name_plural = _("AI")

    def get_absolute_url(self):
        return reverse("AnalogInput_detail", kwargs={"pk": self.pk})


class BinaryInput(InputOutput):
    
    def value(self):
        if self.origin_value is None:
            return False
        if self.origin_value =="0":
            return False
        return True
    
    class Meta:
        verbose_name = _("BI")
        verbose_name_plural = _("BI")

    def __str__(self):
        return f'{self.pk} - {self.com_server.name} . BI [ {self.register} ] = {self.value}'

    def save(self):
        self.child_class='binaryinput'
        super(BinaryInput,self).save()
    def get_absolute_url(self):
        return reverse("AnalogInput_detail", kwargs={"pk": self.pk})


class BinaryOutput(InputOutput):
    employee=models.ForeignKey("employee", verbose_name=_("profile"), on_delete=models.CASCADE)
    value=models.BooleanField(_("value"))
    def write(self,user,value):
        from . import modbus
        com_server=self.com_server
        host=com_server.ip1
        port=com_server.port1
        # address=self.component.feeder().address
        register=self.register
        m=modbus.LeoModbus(user=user)
        m.connect(host=host,port=port)
        m.write_single_coil(address=register,value=value)
        # modbus.modbus_write(host=host,port=port,address=address,register=register,command=command)
 
    def save(self,user=None):
        status=LogStatusEnum.ACTIVED
        description="description"
        title="BinaryCommand SAVE LOG "
        from authentication.repo import ProfileRepo
        profile=ProfileRepo(user).me
        log=Log(title=title,profile=profile,com_server=self.com_server,register=self.register,status=status,description=description)
        log.save()        
        super(BinaryOutput,self).save()


    class Meta:
        verbose_name = _("BinaryCommand")
        verbose_name_plural = _("BinaryCommands")

    def __str__(self):
        return f'{self.com_server.name} ====>   {self.employee.profile.name}  @  { self.date_added} \  {self.value}'

    def get_absolute_url(self):
        return reverse("AnalogInput_detail", kwargs={"pk": self.pk})


class Log(models.Model):
    title=models.CharField(_("title"), max_length=500)
    employee=models.ForeignKey("Employee", verbose_name=_("employee"),null=True,blank=True, on_delete=models.CASCADE)
    com_server=models.ForeignKey("comserver", verbose_name=_("com_server"),null=True,blank=True, on_delete=models.CASCADE)
    register=models.IntegerField(_("register"),default=0)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    status=models.CharField(_("status"),choices=LogStatusEnum.choices, max_length=50)
    # priority=models.CharField(_("status"),choices=LogPriority.choices, max_length=50)
    description=models.CharField(_("description"),null=True,blank=True, max_length=5000)
     
    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":log", kwargs={"pk": self.pk})

class CurrentTransformer(models.Model):
    feeder=models.ForeignKey("feeder", verbose_name=_("feeder"), on_delete=models.CASCADE)
    data_i_a=[]
    data_i_b=[]
    data_i_c=[]
    data1=56
    def value_i_a(self):
        return self.data_i_a[0].value()
    def value_i_a(self):
        return self.data_i_b[0].value()
    def value_i_a(self):
        return self.data_i_c[0].value()
    class Meta:
        verbose_name = _("CurrentTransformer")
        verbose_name_plural = _("CurrentTransformers")

    def __str__(self):
        return self.feeder.name+":ct"
 
    def update_data(self):
        self.data_i_a=AnalogInput.objects.filter(com_server=self.feeder.com_server).filter(register=self.feeder.address+self.feeder.register_ct_i_a).order_by('-date_added')
        self.data_i_b=AnalogInput.objects.filter(com_server=self.feeder.com_server).filter(register=self.feeder.address+self.feeder.register_ct_i_b).order_by('-date_added')
        self.data_i_c=AnalogInput.objects.filter(com_server=self.feeder.com_server).filter(register=self.feeder.address+self.feeder.register_ct_i_c).order_by('-date_added')
    
    def value_i_a(self):
        return self.data_i_a.first().value()
    def value_i_b(self):
        return self.data_i_b.first().value()
    def value_i_c(self):
        return self.data_i_c.first().value()
    
