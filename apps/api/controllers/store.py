from apps.api.models.store import Store
from rest_framework import serializers
from apps.admin.utils.exception_handling import ExceptionHandler

class StoreSerializer(serializers.ModelSerializer):
  from apps.api.controllers.asset import AssetSerializer

  pk                  = serializers.Field(source='pk')
  seller              = serializers.Field(source='seller.id')

  #MODEL METHODS AND PROPERTIES
  url                 = serializers.SerializerMethodField('get_url')

  def get_url(self, obj): return obj.get_absolute_url()

  class Meta:
    model = Store
    fields = ('pk', 'seller',
              'title', 'color',
              'url',)


from rest_framework import filters
from rest_framework import generics
#from apps.api.controllers.listing_filter import StoreFilter

class StoreList(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    #filter_class = StoreFilter
    filter_backends = (filters.DjangoFilterBackend,)
    paginate_by = 6
    paginate_by_param = 'page_size'
    max_paginate_by = 18

class StoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer