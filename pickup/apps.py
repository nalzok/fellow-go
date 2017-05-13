from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PickupConfig(AppConfig):
    name = 'pickup'
    verbose_name = _('pickup')
