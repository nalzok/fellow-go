from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from django_filters.views import FilterView

from .models import Order
from .filters import OrderFilter


class HomePageView(TemplateView):

    template_name = 'index.html'


class OrderFilterView(LoginRequiredMixin, FilterView):
    filterset_class = OrderFilter
    paginate_by = 15


class OrderDetailView(LoginRequiredMixin, DetailView):

    model = Order
