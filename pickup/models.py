import re

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import (
    ugettext_lazy as _, pgettext_lazy
)


class FellowManager(BaseUserManager):
    def create_user(self, stu_id, first_name, last_name, tel, pay_method,
                    password=None, **extra_fields):

        if not stu_id:
            raise ValueError('Users must have a student ID')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not tel:
            raise ValueError('Users must have a telephone number')
        if not pay_method:
            raise ValueError('Users must have a method of pay')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        email = extra_fields.get('email') or (stu_id + '@ecnu.cn')
        extra_fields['email'] = self.normalize_email(email)

        fellow = self.model(
            stu_id=stu_id,
            first_name=first_name,
            last_name=last_name,
            tel=tel,
            pay_method=pay_method,
            **extra_fields
        )

        fellow.set_password(password)
        fellow.save(using=self._db)
        return fellow

    def create_superuser(self, stu_id, first_name, last_name, tel, pay_method,
                         password, **extra_fields):

        fellow = self.create_user(
            stu_id=stu_id,
            first_name=first_name,
            last_name=last_name,
            tel=tel,
            pay_method=pay_method,
            password=password,
            **extra_fields
        )
        fellow.is_staff = True
        fellow.is_superuser = True
        fellow.save(using=self._db)
        return fellow


class Fellow(AbstractBaseUser, PermissionsMixin):

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

    is_staff = models.BooleanField(
        pgettext_lazy('override default', 'staff status'),
        default=False,
        help_text=pgettext_lazy(
            'override default',
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_active = models.BooleanField(
        pgettext_lazy('override default', 'active'),
        default=True,
        help_text=pgettext_lazy(
            'override default',
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = FellowManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'stu_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'tel', 'pay_method']

    class Meta:
        verbose_name = _('fellow')
        verbose_name_plural = _('fellows')

    def __str__(self):
        return _('fellow') + ' ' + self.stu_id

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        contains_chinese = re.findall(r'[\u4e00-\u9fff]+',
                                      self.first_name + self.last_name)
        full_name = ('%s%s' if contains_chinese else '%s %s') % (
        self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.get_full_name()

    @staticmethod
    def forge_fellows(count=1):

        from random import seed, choice
        from uuid import uuid4

        from django.db import IntegrityError
        import forgery_py

        seed()
        for i in range(count):
            try:
                Fellow.objects.create_user(
                    stu_id=str(uuid4()),
                    first_name=forgery_py.name.first_name(),
                    last_name=forgery_py.name.last_name(),
                    tel=forgery_py.address.phone(),
                    pay_method=choice(
                        ['ALIPAY', 'WECHAT', 'QQ']
                    ),
                )
            except IntegrityError as err:
                print(str(err))


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

    def is_expired(self):
        return self.time_expire <= timezone.now()

    def is_available(self):
        return not self.is_expired() and not self.is_taken

    @staticmethod
    def forge_orders(count=1):

        from random import seed, random, randrange, choice

        from django.db import IntegrityError
        import forgery_py

        seed()
        for i in range(count):
            try:
                Order.objects.create(
                    title=forgery_py.lorem_ipsum.title(),
                    body=forgery_py.lorem_ipsum.sentences(),
                    bounty_size=max(30 * random() - 20, 0),
                    maker=Fellow.objects.get(
                        pk=randrange(1, Fellow.objects.count())
                    ),
                    address=forgery_py.address.street_name(),
                    time_expire=timezone.make_aware(
                        forgery_py.date.datetime(),
                        timezone.get_current_timezone()
                    ),
                    is_taken=choice([True, False]),
                    is_completed=choice([True, False]),
                )
            except IntegrityError as err:
                print(str(err))
