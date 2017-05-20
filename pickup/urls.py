from django.conf.urls import url

from haystack.views import search_view_factory

from . import views

app_name = 'pickup'

urlpatterns = [
    url(r'^$',
        views.OrderFilterView.as_view(),
        name='order-list'),
    url(r'^detail/(?P<pk>[0-9])/$',
        views.OrderFilterView.as_view(),
        name='order-detail'),
    url(r'^search/$', search_view_factory(
        view_class=views.AdvancedSearchView.as_view,
    ), name='haystack-search')
]