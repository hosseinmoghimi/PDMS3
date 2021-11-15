from django.utils.translation import gettext as _
from django.db.models import TextChoices

class VoltageLevelEnum(TextChoices):
    MV='MEDIUM_VOLTAGE',_('MEDIUM_VOLTAGE')
    LV='LOW_VOLTAGE',_('LOW_VOLTAGE')
    HV='HIGH_VOLTAGE',_('HIGH_VOLTAGE')

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