from django.test import TestCase

from pickup.forms import AdminFellowCreationForm

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
