from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from pickup.models import Fellow, Order


class AdminFellowCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput)

    class Meta:
        model = Fellow
        fields = ('stu_id', 'first_name', 'last_name', 'tel', 'pay_method', 'nickname', 'email')

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
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_('Password'))

    class Meta:
        model = Fellow
        fields = ('stu_id', 'first_name', 'last_name', 'tel', 'pay_method', 'nickname', 'email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class FellowAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = AdminFellowChangeForm
    add_form = AdminFellowCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('stu_id', 'is_admin')
    list_filter = ('is_admin',)
    # add_fieldsets is not a standard ModelAdmin attribute. FellowAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('stu_id', 'password1', 'password2')}
        ),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'tel')}),
        (_('Payment preferences'),
         {'fields': ('pay_method', 'alipay', 'wechat', 'qq')}),
        (_('Other info'),
         {'fields': ('nickname', 'email')}),
    )
    fieldsets = (
        (None,
         {'fields': ('stu_id', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'tel')}),
        (_('Payment preferences'),
         {'fields': ('pay_method', 'alipay', 'wechat', 'qq')}),
        (_('Other info'),
         {'fields': ('nickname', 'email')}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_admin',)}),
    )
    search_fields = ('stu_id', 'first_name', 'last_name')
    ordering = ('stu_id',)
    filter_horizontal = ()

# Now register the new FellowAdmin...
admin.site.register(Fellow, FellowAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

class OrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)

admin.site.site_header = _('Fellow Go Background')
admin.site.site_title = _('Fellow Go Background')
admin.site.index_title = _('Site Administration')