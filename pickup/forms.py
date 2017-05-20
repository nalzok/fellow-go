from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from datetimewidget.widgets import DateTimeWidget
from haystack.forms import SearchForm


class OrderSearchForm(SearchForm):
    q = forms.CharField(required=False, label=_('Keywords'),
                        widget=forms.TextInput(attrs={'type': 'search'}))

    time_created_start = forms.DateTimeField(
        label=_('Creation time is after'),
        widget=DateTimeWidget(
            attrs={
                'id': 'id_time_created_0',
            },
            usel10n=True,
            bootstrap_version=3
        ),
        required=False
    )
    time_created_end = forms.DateTimeField(
        label=_('Creation time is before'),
        widget=DateTimeWidget(
            attrs={
                'id': 'id_time_created_1',
            },
            usel10n=True,
            bootstrap_version=3
        ),
        required=False
    )

    time_expire_start = forms.DateTimeField(
        label=_('Expiration time is after'),
        widget=DateTimeWidget(
            attrs={
                'id': 'id_time_expire_0',
            },
            usel10n=True,
            bootstrap_version=3
        ),
        required=False
    )
    time_expire_end = forms.DateTimeField(
        label=_('Expiration time is before'),
        widget=DateTimeWidget(
            attrs={
                'id': 'id_time_expire_1',
            },
            usel10n=True,
            bootstrap_version=3
        ),
        required=False
    )

    BOOLEAN_OPTIONS = [
        ('any', _('Any')),
        (True, _('Yes')),
        (False, _('No'))
    ]
    is_taken = forms.ChoiceField(
        label=_('Order is taken?'),
        widget=forms.Select(),
        choices=BOOLEAN_OPTIONS,
        required=False,
    )
    is_completed = forms.ChoiceField(
        label=_('Order is completed?'),
        widget=forms.Select(),
        choices=BOOLEAN_OPTIONS,
        required=False,
    )

    def search(self):
        sqs = super(OrderSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['time_created_start']:
            sqs = sqs.filter(
                time_created__gte=self.cleaned_data['time_created_start'])

        if self.cleaned_data['time_created_end']:
            sqs = sqs.filter(
                time_created__lte=self.cleaned_data['time_created_end'])

        if self.cleaned_data['time_expire_start']:
            sqs = sqs.filter(
                time_expire__gte=self.cleaned_data['time_expire_start'])

        if self.cleaned_data['time_expire_end']:
            sqs = sqs.filter(
                time_expire__lte=self.cleaned_data['time_expire_end'])

        if self.cleaned_data['is_taken'] != 'any':
            sqs = sqs.filter(is_taken=self.cleaned_data['is_taken'])

        if self.cleaned_data['is_completed'] != 'any':
            sqs = sqs.filter(is_completed=self.cleaned_data['is_completed'])

        return sqs
