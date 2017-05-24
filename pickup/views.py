from crispy_forms.bootstrap import InlineField
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from django_filters.views import FilterView
from haystack.generic_views import SearchView

from pickup.models import Order
from pickup.filters import OrderFilter
from pickup.forms import OrderSearchForm


class HomePageView(TemplateView):
    """
    The model view for the homepage
    """
    template_name = 'index.html'


class OrderFilterView(LoginRequiredMixin, FilterView):
    """
    A model view for filter order objects.  This takes the place of a
    list view.
    """
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
    """
    A model view for displaying information about a specific order object.
    """
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class OrderSearchView(LoginRequiredMixin, SearchView):
    """
    A model view for searching for order objects. Searching is based on
    keywords, and can be further filtered by creation date, expiration
    date, and availability.
    """
    template_name = 'search/order_search.html'
    form_class = OrderSearchForm

    def get_context_data(self, *args, **kwargs):
        # Preserving GET arguments with pagination
        # Taken from https://djangosnippets.org/snippets/1592/
        context = super(OrderSearchView, self).get_context_data(*args,
                                                                **kwargs)

        queries_without_page = self.request.GET.copy()
        if 'page' in queries_without_page:
            del queries_without_page['page']
        context['queries'] = queries_without_page

        context['count'] = self.get_queryset().count()

        return context


def common_request_parameters(request):
    """
    Expose extra context variables to all templates.
    """
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