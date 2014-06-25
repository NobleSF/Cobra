from apps.admin.models.category import Category
from rest_framework import serializers
from apps.admin.utils.exception_handling import ExceptionHandler
from rest_framework import filters
from rest_framework import generics
import django_filters

class CategorySerializer(serializers.ModelSerializer):
  from apps.api.controllers.product import ProductSerializer

  pk                  = serializers.Field(source='pk')
  parent_category     = serializers.Field(source='parent_category.name')

  #MODEL METHODS AND PROPERTIES
  url                 = serializers.SerializerMethodField('get_url')

  #SERIALIZERS
  #photos              = serializers.SerializerMethodField('get_photos')

  def get_url(self, obj): return obj.get_absolute_url()

  class Meta:
    model = Category
    fields = ('pk', 'parent_category',
              'name', 'plural_name', 'keywords',)


class CategoryFilter(django_filters.FilterSet):
  category = django_filters.CharFilter(name='name')
  #parents only

  class Meta:
    model = Category
    fields = ['category',]

class CategoryList(generics.ListCreateAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  #filter_class = CategoryFilter
  filter_backends = (filters.DjangoFilterBackend,)
  paginate_by = 8
  paginate_by_param = 'page_size'
  #max_paginate_by = 100

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
