from crispy_forms.bootstrap import InlineField
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from django_filters.views import FilterView
from haystack.generic_views import SearchView

from .models import Order
from .filters import OrderFilter
from .forms import OrderSearchForm


class HomePageView(TemplateView):

    template_name = 'index.html'


class OrderFilterView(LoginRequiredMixin, FilterView):

    filterset_class = OrderFilter
    paginate_by = 15

    def get_context_data(self, *args, **kwargs):
        # https://djangosnippets.org/snippets/1592/
        context = super(OrderFilterView, self).get_context_data(*args,
                                                                **kwargs)

        queries_without_page = self.request.GET.copy()
        if 'page' in queries_without_page:
            del queries_without_page['page']
        context['queries'] = queries_without_page

        return context


class OrderDetailView(LoginRequiredMixin, DetailView):

    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class OrderSearchView(LoginRequiredMixin, SearchView):
    template_name = 'search/order_search.html'
    form_class = OrderSearchForm

    def get_context_data(self, *args, **kwargs):
        # https://djangosnippets.org/snippets/1592/
        context = super(OrderSearchView, self).get_context_data(*args,
                                                                **kwargs)

        queries_without_page = self.request.GET.copy()
        if 'page' in queries_without_page:
            del queries_without_page['page']
        context['queries'] = queries_without_page

        context['count'] = self.get_queryset().count()

        return context


def common_request_parameters(request):
    form = OrderSearchForm()
    form.helper.form_class = 'navbar-form navbar-right'
    form.helper.form_method = 'get'
    form.helper.form_action = reverse('pickup:haystack-search')
    form.helper.layout = Layout(
        InlineField('q')
    )

    return {
        'nav_search_form': form
    }