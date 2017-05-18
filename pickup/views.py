from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Order


class HomePageView(TemplateView):

    template_name = 'index.html'


class OrderListView(LoginRequiredMixin, ListView):

    model = Order
    paginate_by = 15


class OrderDetailView(LoginRequiredMixin, DetailView):

    model = Order
