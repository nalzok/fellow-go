from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Fellow, Order
from .forms import AdminFellowCreationForm, AdminFellowChangeForm


class FellowAdmin(BaseUserAdmin):
    """
    The ModelAdmin object for Fellow
    """
    form = AdminFellowChangeForm
    add_form = AdminFellowCreationForm

    list_display = (
        'stu_id', 'first_name', 'last_name', 'is_staff', 'is_superuser',
        'date_joined'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('stu_id', 'password1', 'password2')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'tel')
        }),
        (_('Payment preferences'), {
            'fields': ('pay_method', 'alipay', 'wechat', 'qq')
        }),
        (_('Other info'), {
            'fields': ('nickname', 'email')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('stu_id', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'tel')
        }),
        (_('Payment preferences'), {
            'fields': ('pay_method', 'alipay', 'wechat', 'qq')
        }),
        (_('Other info'), {
            'fields': ('nickname', 'email')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )
    search_fields = ('stu_id', 'first_name', 'last_name')
    ordering = ('stu_id',)
    filter_horizontal = ()

admin.site.register(Fellow, FellowAdmin)

class OrderAdmin(admin.ModelAdmin):
    """
    The ModelAdmin object for Order
    """
    list_display = (
        'title', 'time_created', 'time_expire', 'is_taken', 'is_completed'
    )

admin.site.register(Order, OrderAdmin)

admin.site.site_header = _('Fellow Go Background')
admin.site.site_title = _('Fellow Go Background')
admin.site.index_title = _('Site Administration')