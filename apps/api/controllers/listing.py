from apps.api.models.listing import Listing
from rest_framework import serializers
from apps.admin.utils.exception_handling import ExceptionHandler
from rest_framework import filters
from rest_framework import generics
import django_filters

class ListingSerializer(serializers.ModelSerializer):
  from apps.api.controllers.product import ProductSerializer

  pk                  = serializers.Field(source='pk')
  product             = serializers.Field(source='product.id')
  category            = serializers.Field(source='category.name')

  #MODEL METHODS AND PROPERTIES
  url                 = serializers.SerializerMethodField('get_url')
  is_sold             = serializers.Field(source='is_sold')
  is_recently_sold    = serializers.Field(source='is_recently_sold')
  metric_dimensions   = serializers.Field(source='metric_dimensions')
  english_dimensions  = serializers.Field(source='english_dimensions')
  pinterest_url       = serializers.Field(source='pinterest_url')

  #SERIALIZERS
  photos              = serializers.SerializerMethodField('get_photos')
  materials           = serializers.SerializerMethodField('get_materials')
  artisans            = serializers.SerializerMethodField('get_artisans')
  colors              = serializers.SerializerMethodField('get_colors')

  def get_photos(self, obj):
    photos = []
    for photo in obj.product.photos.exclude(is_progress=True):
      #url = photo.original
      #cloudinary_id = url[url.rfind('/')+1:url.rfind('.')]
      photos.append(photo.product_size)
    return photos

  def get_materials(self, obj):
    from apps.api.controllers.asset import AssetSerializer
    serializer = AssetSerializer(obj.materials)
    return serializer.data

  def get_artisans(self, obj):
    from apps.api.controllers.asset import AssetSerializer
    serializer = AssetSerializer(obj.product.assets.filter(ilk='artisans'))
    return serializer.data

  def get_colors(self, obj):
    color_list = []
    try:
      for color in obj.product.colors.all():
        color_list.append(color.name)
    except: pass
    return color_list

  def get_url(self, obj): return obj.get_absolute_url()

  class Meta:
    model = Listing
    fields = ('pk', 'product', 'title', 'category', 'description',
              'usd_price', 'local_price', 'us_shipping_price', 'local_shipping_price',
              'is_orderable', 'created_at', 'updated_at',
              'is_sold', 'is_recently_sold',
              'metric_dimensions', 'english_dimensions',
              'pinterest_url', 'url',
              'photos', 'materials', 'artisans', 'colors',)

class ListingFilter(django_filters.FilterSet):

  def limit(queryset, value):
    return queryset[:value]

  limit     = django_filters.NumberFilter(action=limit)

  product   = django_filters.NumberFilter(name='product__id')
  store     = django_filters.NumberFilter(name='product__seller__id')
  category  = django_filters.CharFilter(name='category__name')

  min_price = django_filters.NumberFilter(name="usd_price", lookup_type='gte')
  max_price = django_filters.NumberFilter(name="usd_price", lookup_type='lte')

  class Meta:
    model = Listing
    fields = ['limit',
              'product', 'store', 'category',
              'min_price', 'max_price']
    #order_by = ['product']

class ListingList(generics.ListCreateAPIView):
  queryset = Listing.objects.all()
  serializer_class = ListingSerializer
  filter_class = ListingFilter
  filter_backends = (filters.DjangoFilterBackend,)
  paginate_by = 24
  paginate_by_param = 'page_size'
  max_paginate_by = 120

class ListingDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Listing.objects.all()
  serializer_class = ListingSerializer
