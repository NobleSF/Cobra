from rest_framework import filters
import django_filters

from apps.api.models.listing import Listing
from apps.api.controllers.listing import ListingSerializer

class ListingFilter(django_filters.FilterSet):
  product = django_filters.NumberFilter(name='product__id')
  store = django_filters.NumberFilter(name='product__seller__id')
  category = django_filters.CharFilter(name='category__name')

  min_price = django_filters.NumberFilter(name="usd_price", lookup_type='gte')
  max_price = django_filters.NumberFilter(name="usd_price", lookup_type='lte')

  class Meta:
    model = Listing
    fields = ['product', 'store', 'category', 'min_price', 'max_price']
    #order_by = ['product']
