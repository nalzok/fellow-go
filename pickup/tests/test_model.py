from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from pickup.models import Fellow, Order


class EndUserTests(TestCase):

    def test_object_representation(self):
        test_fellow = Fellow.objects.create(stu_id='001',
                                       password='Tr0ub4dor&3',
                                       first_name='李',
                                       last_name='狗蛋',
                                       tel='001',
                                       pay_method='ALIPAY')
        expected_object_name = _('fellow') + ' ' + test_fellow.stu_id
        self.assertEqual(str(test_fellow), expected_object_name)


class OrderTests(TestCase):

    def test_object_representation(self):
        test_fellow_1 = Fellow.objects.create(stu_id='001',
                                              password='Tr0ub4dor&3',
                                              first_name='李',
                                              last_name='狗蛋',
                                              tel='001',
                                              pay_method='WECHAT')
        test_fellow_2 = Fellow.objects.create(stu_id='002',
                                              password='Tr0ub4dor&3',
                                              first_name='李狗',
                                              last_name='蛋',
                                              tel='002',
                                              pay_method='QQ')
        order = Order.objects.create(title="About Fellow Go",
                                     body="It's awesome!",
                                     bounty_size=0,
                                     time_expire=timezone.now(),
                                     maker=test_fellow_1,
                                     taker=test_fellow_2)
        expected_object_name = _('order') + ' ' + order.title
        self.assertEqual(str(order), expected_object_name)