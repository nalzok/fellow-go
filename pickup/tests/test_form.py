from django.test import TestCase

from pickup.forms import (
    AdminFellowCreationForm, AdminFellowChangeForm, OrderSearchForm
)


class AdminFellowCreationFormTest(TestCase):

    def test_valid_input(self):
        form_data = {
            'stu_id': "001",
            'first_name': "Ben",
            'last_name': "Bitdiddle",
            'tel': "10000",
            'pay_method': "WECHAT",
            'password1': "Tr0ub4dor&3",
            'password2': "Tr0ub4dor&3",
        }
        form = AdminFellowCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_lack_required_fields(self):
        form_data = {
            'password1': "Tr0ub4dor&3",
            'password2': "Tr0ub4dor&3",
        }
        form = AdminFellowCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_passwords_mismatch(self):
        form_data = {
            'stu_id': "001",
            'first_name': "Ben",
            'last_name': "Bitdiddle",
            'tel': "10000",
            'pay_method': "WECHAT",
            'password1': "Tr0ub4dor&3",
            'password2': "Tr0ub4dor&",
        }
        form = AdminFellowCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class AdminFellowChangeFormTest(TestCase):

    def test_valid_input(self):
        form_data = {
            'stu_id': "001",
            'password': "Tr0ub4dor&3",
            'first_name': "Ben",
            'last_name': "Bitdiddle",
            'tel': "10000",
            'pay_method': "WECHAT",
        }
        form = AdminFellowChangeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_lack_required_fields(self):
        form_data = {
            'stu_id': "001",
            'password': "Tr0ub4dor&3",
            'first_name': "Ben",
            'last_name': "Bitdiddle",
            'tel': "10000",
        }
        form = AdminFellowCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class OrderSearchFormTest(TestCase):

    def test_valid_input(self):
        form_data = {
            'q': "keyword"
        }
        form = OrderSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
