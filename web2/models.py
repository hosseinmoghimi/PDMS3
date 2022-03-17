
from utility.persian import PersianCalendar
from django.db import models
from django.forms.fields import CharField
from django.shortcuts import reverse
from django.utils.translation import gettext as _

from pdms.server_settings import COM_SERVER_IS_CONNECTED, STATIC_URL
from .constants import *
from .enums import CircuitBreakerStatusEnum, ComServerOperationCodeEnum, ComServerRedundancyEnum, FeederComponentNameEnum, InputOutputStatusEnum,LogStatusEnum, VoltageLevelEnum
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

class ComServerDataBlock(models.Model):
    com_server=models.ForeignKey("comserver", verbose_name=_("comserver"), on_delete=models.CASCADE)
    start_address=models.IntegerField(_("start_address"),default=1)
    count=models.IntegerField(_("count"),default=1)
    code_name=models.CharField(_("code"),choices=ComServerOperationCodeEnum.choices, max_length=50)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_updated=models.DateTimeField(_("date_updated"), auto_now=True, auto_now_add=False)
    class Meta:
        verbose_name = 'ComServerDataBlock'
        verbose_name_plural = 'ComServerDataBlocks'
    def __str__(self):
        return f"{self.com_server.name}:{self.code_name} {self.start_address}-{self.start_address+self.count}"
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    
class ComServer(models.Model):
    name=models.CharField(_("name"), max_length=50)
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
    # def color(self):
    #     return "primary"
    
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
    current_transformers_ratio=models.IntegerField(_("feeder_current_transformers_ratio") ,default=60)
    com_server=models.ForeignKey("comserver", verbose_name=_("com_server"), on_delete=models.CASCADE)
    # address=models.IntegerField(_("address"),default=0)
    priority=models.IntegerField(_("priority"),default=100)
    bus=models.ForeignKey("bus", verbose_name=_("bus"), on_delete=models.CASCADE)
    voltage_transformers_ratio=models.IntegerField(_("feeder_voltage_transformers_ratio") ,default=350)
    
    register_cb_open=models.IntegerField(_("register_cb_open"),default=REGISTER_CIRCUIT_BREAKER_OPEN)
    register_cb_close=models.IntegerField(_("register_cb_close"),default=REGISTER_CIRCUIT_BREAKER_CLOSE)
    register_cb_test=models.IntegerField(_("register_cb_test"),default=REGISTER_CIRCUIT_BREAKER_TEST)
    register_cb_trip=models.IntegerField(_("register_cb_trip"),default=REGISTER_CIRCUIT_BREAKER_TRIP)
    register_cb_servive=models.IntegerField(_("register_cb_servive"),default=REGISTER_CIRCUIT_BREAKER_SERVICE)
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

    register_power_factor=models.IntegerField(_("register_power_factor"),default=REGISTER_POWER_FACTOR)

    circuit_breaker_status=models.CharField(_("circuit_breaker_status"),choices=CircuitBreakerStatusEnum.choices,default=CircuitBreakerStatusEnum.TEST, max_length=50)
    i_a=models.IntegerField(_("I a"),null=True,blank=True)
    i_b=models.IntegerField(_("I b"),null=True,blank=True)
    i_c=models.IntegerField(_("I c"),null=True,blank=True)

    v_a=models.IntegerField(_("V a"),null=True,blank=True)
    v_b=models.IntegerField(_("V b"),null=True,blank=True)
    v_c=models.IntegerField(_("V c"),null=True,blank=True)

    v_ab=models.IntegerField(_("V ab"),null=True,blank=True)
    v_bc=models.IntegerField(_("V bc"),null=True,blank=True)
    v_ac=models.IntegerField(_("V ac"),null=True,blank=True)


    
    p=models.IntegerField(_("p"),null=True,blank=True)
    q=models.IntegerField(_("q"),null=True,blank=True)
    s=models.IntegerField(_("s"),null=True,blank=True)

    power_factor=models.IntegerField(_("power_factor"),null=True,blank=True)


    class_name="feeder"

     
    
    def update_circuit_breaker_status(self):
        status=CircuitBreakerStatusEnum.FAILED
        try:
            cb_open=BinaryComponent.objects.filter(feeder=self).filter(name=FeederComponentNameEnum.REGISTER_CB_OPEN).order_by('-date_added').first().value()
            cb_close=BinaryComponent.objects.filter(feeder=self).filter(name=FeederComponentNameEnum.REGISTER_CB_CLOSE).order_by('-date_added').first().value()
            cb_test=BinaryComponent.objects.filter(feeder=self).filter(name=FeederComponentNameEnum.REGISTER_CB_TEST).order_by('-date_added').first().value()
            cb_trip=BinaryComponent.objects.filter(feeder=self).filter(name=FeederComponentNameEnum.REGISTER_CB_TRIP).order_by('-date_added').first().value()
            if cb_close:
                status= CircuitBreakerStatusEnum.CLOSE
            if cb_open:
                status= CircuitBreakerStatusEnum.OPEN
            if cb_test:
                status= CircuitBreakerStatusEnum.TEST
            if cb_trip:
                status= CircuitBreakerStatusEnum.TRIP
                
       

        except:
            pass    
        # import random
        
        # status=CircuitBreakerStatusEnum.choices[random.randint(0,3)][0]
        self.circuit_breaker_status=status
        self.save()
        return status
    
    def create_sample_date_analog_input(self):
        import random
        registers_ct=[
            self.register_ct_i_a,
            self.register_ct_i_b,
            self.register_ct_i_c,
        ]
        registers_vt=[

            self.register_vt_v_a,
            self.register_vt_v_b,
            self.register_vt_v_c,

        ]
        for register in registers_ct:
            ai=AnalogInput()
            ai.register=self.address+register
            ai.com_server=self.com_server
            ai.status=InputOutputStatusEnum.INVALID
            ai.status=InputOutputStatusEnum.SUCCESSFULL
            ai.origin_value=str(random.randint(self.current_transformers_ratio*0.6,self.current_transformers_ratio*0.9))
            # print(ai.origin_value)
            # print(10*"#@#$")
            ai.save()

        
        for register in registers_vt:
            ai=AnalogInput()
            ai.register=self.address+register
            ai.com_server=self.com_server
            ai.status=InputOutputStatusEnum.INVALID
            ai.status=InputOutputStatusEnum.SUCCESSFULL
            ai.origin_value=str(random.randint(self.voltage_transformers_ratio*0.6,self.voltage_transformers_ratio*0.9))
            # print(ai.origin_value)
            # print(10*"#@#$")
            ai.save()
    
    def circuit_breaker_schematic(self):
        self.update_circuit_breaker_status()
        status=self.circuit_breaker_status
        if status==CircuitBreakerStatusEnum.OPEN and self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-open.png'
        if status==CircuitBreakerStatusEnum.TEST and self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-test.png'
        if status==CircuitBreakerStatusEnum.TRIP and self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-trip.png'
        if status==CircuitBreakerStatusEnum.TRIP and not self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-trip-dead.png'
        if status==CircuitBreakerStatusEnum.CLOSE and self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-close.png'
        if status==CircuitBreakerStatusEnum.OPEN and not self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-open-dead.png'
        if status==CircuitBreakerStatusEnum.CLOSE and not self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-close-dead.png'

        if status==CircuitBreakerStatusEnum.FAILED and self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-failed.png'
        if status==CircuitBreakerStatusEnum.FAILED  and not self.bus.is_live:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-failed-dead.png'
        if status==CircuitBreakerStatusEnum.TEST:
            return f'{STATIC_URL}{APP_NAME}/img/circuit-breaker-test.png'
        
       
    def earth_schematic(self):
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
        if status==CircuitBreakerStatusEnum.TEST:
            return f'{STATIC_URL}{APP_NAME}/img/cb-testing.png'
    
    def parameters_schematic(self):
        return f"""
        <div>
            <h5>I a = {self.i_a} <small class="text-muted">Ampere</small></h5>
            <h5>I b = {self.i_b} <small class="text-muted">Ampere</small></h5>
            <h5>I c = {self.i_c} <small class="text-muted">Ampere</small></h5>
        </div>
        """
       
    def panel(self):
        # return ""
        components_panels=""
        components_panels+=f"""<div><img src="{self.circuit_breaker_schematic()}" width="100"></div>"""
        # components_panels+=self.current_transformer.panel()
        return f"""
            <div>
            
            {components_panels}
            <h5>
            <a href="{self.get_absolute_url()}">
            
            {self.name}
            </a>
            </h5>
            </div>
        """
    
    def panel_for_bus_view(self):
        # return ""
        components_panels=""
        components_panels+=f"""<div class="text-center"><a href="{self.get_absolute_url()}" target="_blank"><h4>{self.name}<h4></a>"""
        components_panels+=f"""<div class="text-center"><img src="{self.circuit_breaker_schematic()}" width="100"></div>"""
        # components_panels+=f"""<div><img src="{self.earth_schematic()}" width="100"></div>"""
        components_panels+=self.parameters_schematic()
        # components_panels+=self.current_transformer.panel()
        return f"""
            <div>
            
            {components_panels}
           
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


    
    def get_last_values(self,count):
        objects=AnalogComponent.objects.filter(feeder=self).order_by("-date_added")
        return {
            
                FeederComponentNameEnum.REGISTER_I_A: objects.filter(name=FeederComponentNameEnum.REGISTER_I_A)[:count],
                FeederComponentNameEnum.REGISTER_I_B: objects.filter(name=FeederComponentNameEnum.REGISTER_I_B)[:count],
                FeederComponentNameEnum.REGISTER_I_C: objects.filter(name=FeederComponentNameEnum.REGISTER_I_C)[:count],
     
                FeederComponentNameEnum.REGISTER_V_A: objects.filter(name=FeederComponentNameEnum.REGISTER_V_A)[:count],
                FeederComponentNameEnum.REGISTER_V_B: objects.filter(name=FeederComponentNameEnum.REGISTER_V_B)[:count],
                FeederComponentNameEnum.REGISTER_V_C: objects.filter(name=FeederComponentNameEnum.REGISTER_V_C)[:count],
        }

class Bus(models.Model):
    area=models.ForeignKey("area", verbose_name=_("area"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=50)
    tip=models.CharField(_("tip"),choices=VoltageLevelEnum.choices,null=True,blank=True, max_length=50)
    brand=models.CharField(_("brand"),null=True,blank=True, max_length=5000)
    model_name=models.CharField(_("model_name"),null=True,blank=True, max_length=5000)
    serial_no=models.CharField(_("serial_no"),null=True,blank=True, max_length=5000)
    description=models.CharField(_("description"),null=True,blank=True, max_length=5000)
    voltage=models.IntegerField(_("voltage"))
    is_live=models.BooleanField(_("is live ?"),default=True)
    class_name="bus"
    def panel(self):
        return f"""
        <div>
        <a target="_blank" href="{self.get_absolute_url()}">
        {self.area.region}-{self.area.name} : {self.name} ({self.tip})
        </a>
        </div>
        """
    def __str__(self):
        return self.name
    def save(self):
        self.child_class="bus"
        super(Bus,self).save()
    class Meta:
        verbose_name = 'Bus'
        verbose_name_plural = 'Buses'
    def get_absolute_url(self):
        return reverse(APP_NAME+":bus",kwargs={'pk':self.pk})
    def get_bus_bar_url(self):
        return reverse(APP_NAME+":bus_bar",kwargs={'bus_id':self.pk})
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
     
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
 

class Permission(models.Model):
    employee=models.ForeignKey("Employee", verbose_name=_("employee"),null=True,blank=True, on_delete=models.CASCADE)
    com_server=models.ForeignKey("comserver", verbose_name=_("comserver"), on_delete=models.CASCADE)
    register=models.IntegerField(_("register"))
    can_read=models.BooleanField(_("can_read"),default=False)
    can_write=models.BooleanField(_("can_write"),default=False)
    class Meta:
        
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
 

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

 
class FeederComponent(models.Model):
    feeder=models.ForeignKey("feeder", verbose_name=_("feeder"), on_delete=models.CASCADE)
    name=models.CharField(_("name"),max_length=100)
    register=models.IntegerField(_("register"),default=0)
    origin_value=models.IntegerField(_("origin_value"))
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("FeederComponent")
        verbose_name_plural = _("FeederComponents")

    def __str__(self):
        return f"""{self.feeder.com_server}:{self.register}:{self.feeder.name} : {self.name}:{self.value()}"""
 
 
    def value(self):
        if self.origin_value is None:
            return False
        return self.origin_value
    def binary_value(self):
        if self.origin_value is None:
            return False
        if self.origin_value==1:
            return True
        if self.origin_value==0:
            return False 
    

class AnalogComponent(FeederComponent):

    class Meta:
        verbose_name = _("AnalogComponent")
        verbose_name_plural = _("AnalogComponents")
    

class BinaryComponent(FeederComponent):

    class Meta:
        verbose_name = _("BinaryComponent")
        verbose_name_plural = _("BinaryComponent")
 
 
    def __str__(self):
        # return f"""{self.feeder.name} : {self.name}: {self.binary_value()}"""
        return f"""{self.feeder.com_server}:{self.register}:{self.feeder.name} : {self.name}:{self.binary_value()}"""
 
 