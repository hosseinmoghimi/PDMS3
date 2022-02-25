from django.utils.translation import gettext as _
from django.db.models import TextChoices

class VoltageLevelEnum(TextChoices):
    MV='MEDIUM_VOLTAGE',_('MEDIUM_VOLTAGE')
    LV='LOW_VOLTAGE',_('LOW_VOLTAGE')
    HV='HIGH_VOLTAGE',_('HIGH_VOLTAGE')
class FeederComponentNameEnum(TextChoices):
    REGISTER_I_A='REGISTER_I_A',_('REGISTER_I_A')
    REGISTER_I_B='REGISTER_I_B',_('REGISTER_I_B')
    REGISTER_I_C='REGISTER_I_C',_('REGISTER_I_C')
    
    REGISTER_V_A='REGISTER_V_A',_('REGISTER_V_A')
    REGISTER_V_B='REGISTER_V_B',_('REGISTER_V_B')
    REGISTER_V_C='REGISTER_V_C',_('REGISTER_V_C')
    
    REGISTER_V_AB='REGISTER_V_AB',_('REGISTER_V_AB')
    REGISTER_V_AC='REGISTER_V_AC',_('REGISTER_V_AC')
    REGISTER_V_BC='REGISTER_V_BC',_('REGISTER_V_BC')
    
    REGISTER_Q='REGISTER_Q',_('REGISTER_Q')
    REGISTER_P='REGISTER_P',_('REGISTER_P')
    REGISTER_S='REGISTER_S',_('REGISTER_S')

class ComServerRedundancyEnum(TextChoices):
    HOT='HOT',_('HOT')
    STAND_BY='STAND_BY',_('STAND_BY')
class InputOutputStatusEnum(TextChoices):
    DISCONNECTED='DISCONNECTED',_('DISCONNECTED')
    SUCCESSFULL='SUCCESSFULL',_('SUCCESSFULL')
    FAILED='FAILED',_('FAILED')
    INVALID='INVALID',_('INVALID')

class LogStatusEnum(TextChoices):
    ENABLED='ENABLE',_('ENABLE')
    DISABLED='DISABLE',_('DISABLE')
    TOGGLE='TOGGLE',_('TOGGLE')
    ACTIVED='ACTIVE',_('ACTIVE')
    INACTIVED='INACTIVE',_('INACTIVE')
    POWER_ON='POWER_ON',_('POWER_ON')
    POWER_OFF='POWER_OFF',_('POWER_OFF')
    START='START',_('START')
    STOP='STOP',_('STOP')
    INSTALLED='INSTALLED',_('INSTALLED')
    REMOVED='REMOVED',_('REMOVED')
    UNABLE_TO_CONNECT='unable to connect !',_('unable to connect !')

class CircuitBreakerStatusEnum(TextChoices):
    OPEN='OPEN',_('OPEN')
    CLOSE='CLOSE',_('CLOSE')
    TESTING='TESTING',_('TESTING')
    FAILED='FAILED',_('FAILED')
class ComServerOperationCodeEnum(TextChoices):
    READ_COILS='READ_COILS',_('READ_COILS')
    WRITE_SINGEL_COIL='WRITE_SINGEL_COIL',_('WRITE_SINGEL_COIL')
    READ_HOLDING_REGISTERS='READ_HOLDING_REGISTERS',_('READ_HOLDING_REGISTERS')