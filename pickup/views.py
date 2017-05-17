from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Order


class HomePageView(TemplateView):
    template_name = 'index.html'


class OrderListView(ListView):
    model = Order

class OrderDetailView(DetailView):
    model = Order
