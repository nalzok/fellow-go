from haystack import indexes

from .models import Order


class OrderIndex(indexes.SearchIndex, indexes.Indexable):
    """
    The search index for orders. This is required by Haystack.
    """
    text = indexes.CharField(document=True, use_template=True)
    time_created = indexes.DateTimeField(model_attr='time_created')
    time_expire = indexes.DateTimeField(model_attr='time_expire')
    is_taken = indexes.BooleanField(model_attr='is_taken')
    is_completed = indexes.BooleanField(model_attr='is_completed')

    def get_model(self):
        return Order

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
