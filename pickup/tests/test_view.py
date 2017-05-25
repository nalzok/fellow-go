from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from pickup.models import Fellow, Order


class HomePageViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)


class OrderFilterViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user to login with
        Fellow.objects.create_user(
            stu_id='001',
            password='Tr0ub4dor&3',
            first_name='Ben',
            last_name='Bitdiddle',
            tel='001',
            pay_method='ALIPAY'
        )
        # Create 21 orders for pagination tests
        Fellow.forge_fellows(count=10)
        Order.forge_orders(count=21)

    def test_redirect_if_not_logged_in_by_url(self):
        resp = self.client.get('/pickup/')
        self.assertEqual(resp.status_code, 302)

    def test_redirect_if_not_logged_in_by_name(self):
        resp = self.client.get(reverse('pickup:order-list'))
        self.assertEqual(resp.status_code, 302)

    def test_view_uses_correct_template(self):
        self.assertTrue(self.client.login(stu_id='001', password='Tr0ub4dor&3'))
        resp = self.client.get(reverse('pickup:order-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pickup/order_filter.html')

    def test_pagination_is_fifteen(self):
        self.assertTrue(self.client.login(stu_id='001', password='Tr0ub4dor&3'))
        resp = self.client.get(reverse('pickup:order-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 15)

    def test_lists_all_orders(self):
        self.assertTrue(self.client.login(stu_id='001', password='Tr0ub4dor&3'))
        # Get second page and confirm it has (exactly) remaining 6 items
        resp = self.client.get(
            reverse('pickup:order-list') + '?page=2',
            follow=True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 6)


class OrderDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user to login with
        Fellow.objects.create_user(
            stu_id='001',
            password='Tr0ub4dor&3',
            first_name='Ben',
            last_name='Bitdiddle',
            tel='001',
            pay_method='ALIPAY'
        )
        Order.forge_orders(count=1)

    def test_redirect_if_not_logged_in_by_url(self):
        resp = self.client.get('/pickup/detail/1/')
        self.assertEqual(resp.status_code, 302)

    def test_redirect_if_not_logged_in_by_name(self):
        resp = self.client.get(reverse('pickup:order-detail', args=[1]))
        self.assertEqual(resp.status_code, 302)

    def test_view_uses_correct_template(self):
        self.assertTrue(self.client.login(stu_id='001', password='Tr0ub4dor&3'))
        resp = self.client.get(reverse('pickup:order-detail', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pickup/order_detail.html')


class OrderSearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user to login with
        Fellow.objects.create_user(
            stu_id='001',
            password='Tr0ub4dor&3',
            first_name='Ben',
            last_name='Bitdiddle',
            tel='001',
            pay_method='ALIPAY'
        )
        # Create two orders to search within
        Order.objects.create(
            title="test_keyword",
            body="test_keyword",
            bounty_size=0,
            maker=Fellow.objects.get(pk=1),
            address="Global village",
            time_expire=timezone.now(),
        )
        Order.objects.create(
            title="irrelevant_title",
            body="irrelevant_body",
            bounty_size=0,
            maker=Fellow.objects.get(pk=1),
            address="Global village",
            time_expire=timezone.now(),
        )

    def test_redirect_if_not_logged_in_by_url(self):
        resp = self.client.get('/pickup/search/?q=test_keyword')
        self.assertEqual(resp.status_code, 302)

    def test_redirect_if_not_logged_in_by_name(self):
        resp = self.client.get("%(url)s?q=%(keyword)s" % {
            'url': reverse('pickup:haystack-search'),
            'keyword': "test_keyword",
        })
        self.assertEqual(resp.status_code, 302)

    def test_view_uses_correct_template(self):
        self.assertTrue(self.client.login(stu_id='001', password='Tr0ub4dor&3'))
        resp = self.client.get("%(url)s?q=%(keyword)s" % {
            'url': reverse('pickup:haystack-search'),
            'keyword': "test_keyword",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'search/order_search.html')

    def test_view_returns_correct_object(self):
        self.assertTrue(self.client.login(stu_id='001', password='Tr0ub4dor&3'))
        resp = self.client.get("%(url)s?q=%(keyword)s" % {
            'url': reverse('pickup:haystack-search'),
            'keyword': "test_keyword",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)
        self.assertTrue(len(resp.context['object_list']) == 1)
        self.assertEqual(resp.context['object_list'][0].object.pk, 1)


class AdminTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user to login with
        Fellow.objects.create_user(
            stu_id='001',
            password='Tr0ub4dor&3',
            first_name='Ben',
            last_name='Bitdiddle',
            tel='001',
            pay_method='ALIPAY'
        )
        # Create a superuser to login with
        Fellow.objects.create_superuser(
            stu_id='002',
            password='Tr0ub4dor&3',
            first_name='Ben',
            last_name='Sysadmin',
            tel='002',
            pay_method='WECHAT'
        )
        # Create 21 orders for pagination tests
        Fellow.forge_fellows(count=10)
        Order.forge_orders(count=21)

    def test_redirect_if_not_logged_in_by_url(self):
        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 302)

    def test_redirect_if_logged_in_not_superuser_by_url(self):
        self.assertTrue(self.client.login(stu_id='001', password='Tr0ub4dor&3'))
        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 302)

    def test_redirect_if_logged_in_superuser_by_url(self):
        self.assertTrue(self.client.login(stu_id='002', password='Tr0ub4dor&3'))
        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 200)
