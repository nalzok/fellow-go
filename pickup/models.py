from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy


class FellowManager(BaseUserManager):

    def create_user(self, stu_id, first_name, last_name, tel, pay_method, password=None):

        if not stu_id:
            raise ValueError('Users must have a student ID')

        fellow = self.model(
            stu_id=stu_id,
            first_name=first_name,
            last_name=last_name,
            tel=tel,
            pay_method=pay_method,
        )

        if not fellow.email:
            fellow.email = fellow.stu_id + '@ecnu.cn'

        fellow.set_password(password)
        fellow.save(using=self._db)
        return fellow

    def create_superuser(self, stu_id, first_name, last_name, tel, pay_method, password):

        user = self.create_user(
            stu_id=stu_id,
            first_name=first_name,
            last_name=last_name,
            tel=tel,
            pay_method=pay_method,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Fellow(AbstractBaseUser):

    stu_id = models.CharField(
        _('student ID'),
        max_length=20,
        unique=True
    )

    first_name = models.CharField(
        pgettext_lazy('override default', 'first name'),
        max_length=30
    )
    last_name = models.CharField(
        pgettext_lazy('override default', 'last name'),
        max_length=150
    )
    tel = models.CharField(
        _('phone'),
        max_length=20,
        unique=True
    )

    PAY_METHOD_CHOICES = (
        ('ALIPAY', _('Alipay')),
        ('WECHAT', _('Wechat')),
        ('QQ', _('QQ')),
    )
    pay_method = models.CharField(
        _('method of pay'),
        max_length=30,
        choices=PAY_METHOD_CHOICES
    )
    alipay = models.CharField(
        _('Alipay account'),
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )
    wechat = models.CharField(
        _('WeChat ID'),
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )
    qq = models.CharField(
        _('QQ ID'),
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    nickname = models.CharField(
        _('nickname'),
        max_length=150,
        blank=True,
        null=True
    )
    email = models.EmailField(
        pgettext_lazy('override default', 'email address'),
        max_length=255,
        blank=True,
        null=True
    )

    balance = models.DecimalField(
        _('balance'),
        max_digits=28,
        decimal_places=2,
        default=0
    )
    is_active = models.BooleanField(_('is active?'), default=True)
    is_admin = models.BooleanField(_('is admin?'), default=False)

    objects = FellowManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'stu_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'tel', 'pay_method']

    class Meta:
        verbose_name = _('fellow')
        verbose_name_plural = _('fellows')

    def __str__(self):
        return _('fellow') + ' ' + self.stu_id

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.get_full_name()


class Order(models.Model):

    title = models.CharField(
        _('order title'),
        max_length=100,
        unique=True
    )

    body = models.CharField(
        _('order body'),
        max_length=500
    )

    bounty_size = models.DecimalField(
        _('amount of bounty'),
        max_digits=28,
        decimal_places=2
    )

    maker = models.ForeignKey(
        Fellow,
        verbose_name=_('orderer'),
        related_name='%(class)s_made',
        on_delete=models.SET_NULL,
        null=True
    )

    address = models.CharField(
        _('address'),
        max_length=200
    )

    taker = models.ForeignKey(
        Fellow,
        verbose_name=_('order taker'),
        related_name='%(class)s_taken',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    time_created = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )

    time_modified = models.DateTimeField(
        _('last modified at'),
        auto_now=True
    )

    time_expire = models.DateTimeField(
        _('valid before')
    )

    is_taken = models.BooleanField(
        _('is already taken?'),
        default=False
    )

    is_completed = models.BooleanField(
        _('is already completed?'),
        default=False
    )

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return _('order') + ' ' + self.title
