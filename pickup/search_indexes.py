from haystack import indexes

from .models import Order


class OrderIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    maker = indexes.CharField(model_attr='maker')
    time_created = indexes.DateTimeField(model_attr='time_created')
    time_expire = indexes.DateTimeField(model_attr='time_expire')

    def get_model(self):
        return Order

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
