from apps.api.models.store import Store
from rest_framework import serializers
from apps.admin.utils.exception_handling import ExceptionHandler
from rest_framework import filters
from rest_framework import generics
import django_filters

class StoreSerializer(serializers.ModelSerializer):
  from apps.api.controllers.asset import AssetSerializer

  pk                  = serializers.Field(source='pk')
  seller              = serializers.Field(source='seller_id')

  #MODEL METHODS AND PROPERTIES
  url                 = serializers.SerializerMethodField('get_url')

  #SERIALIZERS
  photos              = serializers.SerializerMethodField('get_photos')
  artisans            = serializers.SerializerMethodField('get_artisans')

  def get_url(self, obj): return obj.get_absolute_url()

  def get_photos(self, obj):
    try: return obj.products[0].photos[0].product_size
    except: return ""

  def get_artisans(self, obj):
    try: return obj.assets.filter(ilk='artisan')
    except: return ""

  class Meta:
    model = Store
    fields = ('pk', 'seller',
              'title', 'color',
              'url',
              'photos', 'artisans',)

class StoreFilter(django_filters.FilterSet):

  def limit(queryset, value):
    return queryset[:value]

  def filter_category(queryset, value):
    if not value: return queryset
    queryset = queryset #...custom filtering on queryset using 'value'...
    return queryset

  limit     = django_filters.NumberFilter(action=limit)
  category  = django_filters.CharFilter(action=filter_category)

  class Meta:
    model = Store
    fields = ['limit', 'category',]

class StoreList(generics.ListCreateAPIView):
  queryset = Store.objects.all()
  serializer_class = StoreSerializer
  filter_class = StoreFilter
  filter_backends = (filters.DjangoFilterBackend,)
  paginate_by = 6
  paginate_by_param = 'page_size'
  max_paginate_by = 18

class StoreDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Store.objects.all()
  serializer_class = StoreSerializer
