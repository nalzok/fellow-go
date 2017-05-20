from django import forms
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from datetimewidget.widgets import DateTimeWidget
import django_filters

from .models import Order


class CustomBooleanWidget(django_filters.widgets.BooleanWidget):
    def __init__(self, attrs=None):
        super(CustomBooleanWidget, self).__init__(attrs)
        self.choices = (('', _('Any')),
                        ('true', _('Yes')),
                        ('false', _('No')))



class OrderFilter(django_filters.FilterSet):
    availability = django_filters.BooleanFilter(
        label=_('Availability'),
        widget=CustomBooleanWidget(),
        method='filter_availability'
    )

    time_created__gt = django_filters.DateTimeFilter(
        name='time_created',
        label=_('Creation time is later than'),
        widget=DateTimeWidget(
            attrs={'id': 'id_time_created_0'},
            usel10n=True,
            bootstrap_version=3
        ),
        lookup_expr='gt'
    )

    time_created__lt = django_filters.DateTimeFilter(
        name='time_created',
        label=_('Creation time is earlier than'),
        widget=DateTimeWidget(
            attrs={'id': 'id_time_created_1'},
            usel10n=True,
            bootstrap_version=3
        ),
        lookup_expr='lt'
    )
    o = django_filters.OrderingFilter(

        label=_('Ordering'),

        choices=(
            ('time_created', _('Creation time (ascending)')),
            ('-time_created', _('Creation time (descending)')),
            ('time_expire', _('Expiration time (ascending)')),
            ('-time_expire', _('Expiration time (descending)')),
            ('bounty_size', _('Amount of bounty (ascending)')),
            ('-bounty_size', _('Amount of bounty (descending)')),
        ),

        fields=(
            ('time_created', 'time_created'),
            ('-time_created', '-time_created'),
            ('time_expire', 'time_expire'),
            ('-time_expire', '-time_expire'),
            ('bounty_size', 'bounty_size'),
            ('-bounty_size', '-bounty_size'),
        ),
    )

    class Meta:
        model = Order
        fields = []

    @property
    def qs(self):
        parent = super(OrderFilter, self).qs
        if hasattr(parent, 'ordered') and not parent.ordered:
            return parent.order_by('-time_created')
        return parent

    def filter_availability(self, qs, name, value):
        if value is True:
            return qs.filter(
                Q(is_taken=False)
                & Q(time_expire__gt=timezone.now())
            )
        else:
            return qs.filter(
                Q(is_taken=True)
                | Q(time_expire__lte=timezone.now())
            )
