from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from django_filters.views import FilterView
from haystack.query import SearchQuerySet
from haystack.generic_views import SearchView

from .models import Order
from .filters import OrderFilter
from .forms import AdvancedSearchForm


class HomePageView(TemplateView):

    template_name = 'index.html'


class OrderFilterView(LoginRequiredMixin, FilterView):
    filterset_class = OrderFilter
    paginate_by = 15


class OrderDetailView(LoginRequiredMixin, DetailView):

    model = Order


class AdvancedSearchView(LoginRequiredMixin, SearchView):
    template_name = 'search/search.html'
    form_class = AdvancedSearchForm

    def get_context_data(self, *args, **kwargs):
        # https://djangosnippets.org/snippets/1592/
        context = super(AdvancedSearchView, self).get_context_data(*args,
                                                                   **kwargs)

        queries_without_page = self.request.GET.copy()
        if 'page' in queries_without_page:
            del queries_without_page['page']
        context['queries'] = queries_without_page

        context['count'] = self.get_queryset().count()

        return context
