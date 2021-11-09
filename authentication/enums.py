from django.db.models import TextChoices
from django.utils.translation import gettext as _


class ProfileStatusEnum(TextChoices):
    ENABLED='فعال',_('فعال')
    DISABLED='غیر فعال',_('غیر فعال')
