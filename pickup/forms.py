from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from datetimewidget.widgets import DateTimeWidget
from haystack.forms import SearchForm

from .models import Fellow


class AdminFellowCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput)

    class Meta:
        model = Fellow
        fields = (
        'stu_id', 'first_name', 'last_name', 'tel', 'pay_method', 'nickname',
        'email', 'is_active', 'is_staff', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AdminFellowChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_('Password'))

    class Meta:
        model = Fellow
        fields = (
        'stu_id', 'first_name', 'last_name', 'tel', 'pay_method', 'nickname',
        'email', 'password', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class OrderSearchForm(SearchForm):
    q = forms.CharField(required=False, label=_('Search keywords'),
                        widget=forms.TextInput(attrs={'type': 'search'}))

    date_time_options = {
        'clearBtn': 'false',
        'pickerPosition': 'bottom-left',
    }

    time_created_start = forms.DateTimeField(
        label=_('Creation time is after'),
        widget=DateTimeWidget(
            attrs={
                'id': 'id_time_created_0',
            },
            usel10n=True,
            bootstrap_version=3,
            options=date_time_options,
        ),
        required=False,
    )
    time_created_end = forms.DateTimeField(
        label=_('Creation time is before'),
        widget=DateTimeWidget(
            attrs={
                'id': 'id_time_created_1',
            },
            usel10n=True,
            bootstrap_version=3,
            options=date_time_options,
        ),
        required=False,
    )

    time_expire_start = forms.DateTimeField(
        label=_('Expiration time is after'),
        widget=DateTimeWidget(
            attrs={
                'id': 'id_time_expire_0',
            },
            usel10n=True,
            bootstrap_version=3,
            options=date_time_options,
        ),
        required=False,
    )
    time_expire_end = forms.DateTimeField(
        label=_('Expiration time is before'),
        widget=DateTimeWidget(
            attrs={
                'id': 'id_time_expire_1',
            },
            usel10n=True,
            bootstrap_version=3,
            options=date_time_options,
        ),
        required=False,
    )

    BOOLEAN_OPTIONS = [
        ('any', _('Any')),
        ('True', _('Yes')),
        ('False', _('No'))
    ]
    is_taken = forms.ChoiceField(
        label=_('Order is taken?'),
        widget=forms.Select(),
        choices=BOOLEAN_OPTIONS,
        required=False,
        disabled=True
    )
    is_completed = forms.ChoiceField(
        label=_('Order is completed?'),
        widget=forms.Select(),
        choices=BOOLEAN_OPTIONS,
        required=False,
        disabled=True
    )

    def __init__(self, *args, **kwargs):
        super(OrderSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

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

        if self.cleaned_data['is_taken'] in ['True', 'False']:
            sqs = sqs.filter(is_taken=self.cleaned_data['is_taken'])

        if self.cleaned_data['is_completed'] in ['True', 'False']:
            sqs = sqs.filter(is_completed=self.cleaned_data['is_completed'])

        return sqs
