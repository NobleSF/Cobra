from django.http import HttpResponse, Http404
from apps.api.models.listing import Listing
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from apps.admin.utils.exception_handling import ExceptionHandler
from django.views.decorators.cache import cache_page

class ListingSerializer(serializers.ModelSerializer):
  from apps.api.controllers.product import ProductSerializer

  pk = serializers.Field(source='pk')
  product_id          = serializers.Field(source='product.id')
  category = serializers.Field(source='category.name')

  #MODEL METHODS AND PROPERTIES
  url                 = serializers.SerializerMethodField('get_url')
  is_sold             = serializers.Field(source='is_sold')
  is_recently_sold    = serializers.Field(source='is_recently_sold')
  metric_dimensions   = serializers.Field(source='metric_dimensions')
  english_dimensions  = serializers.Field(source='english_dimensions')
  pinterest_url       = serializers.Field(source='pinterest_url')

  #SERIALIZERS
  photos = serializers.SerializerMethodField('get_photos')
  materials = serializers.SerializerMethodField('get_materials')
  artisans = serializers.SerializerMethodField('get_artisans')
  colors = serializers.SerializerMethodField('get_colors')

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
    fields = ('pk', 'product_id', 'title', 'category', 'description',
              'usd_price', 'local_price', 'us_shipping_price', 'local_shipping_price',
              'is_orderable', 'created_at', 'updated_at',
              'is_sold', 'is_recently_sold',
              'metric_dimensions', 'english_dimensions',
              'pinterest_url', 'url',
              'photos', 'materials', 'artisans', 'colors',)


#http://www.django-rest-framework.org/tutorial/3-class-based-views#using-generic-class-based-views
from rest_framework import filters
from rest_framework import generics
from apps.api.controllers.listing_filter import ListingFilter

class ListingList(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_class = ListingFilter
    filter_backends = (filters.DjangoFilterBackend,)

class ListingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


#CLASS BASED VIEW WITH FUNCTION FOR EACH HTTP METHOD

#class ListingList(APIView):
#  """
#  List all listings, or create a new listing.
#  """
#  def get(self, request, format=None):
#    listings = Listing.objects.all()
#    serializer = ListingSerializer(listings, many=True)
#    return Response(serializer.data)
#
#  def post(self, request, format=None):
#    serializer = ListingSerializer(data=request.DATA)
#    if serializer.is_valid():
#      serializer.save()
#      return Response(serializer.data, status=status.HTTP_201_CREATED)
#    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#class ListingDetail(APIView):
#  """
#  Retrieve, update or delete a listing.
#  """
#  def get_object(self, product_id):
#    try:
#      return Listing.objects.get(product_id=product_id)
#    except Listing.DoesNotExist:
#      raise Http404
#
#  def get(self, request, product_id, format=None):
#    listing = self.get_object(product_id)
#    serializer = ListingSerializer(listing)
#    return Response(serializer.data)
#
#  def put(self, request, product_id, format=None):
#    listing = self.get_object(product_id)
#    serializer = ListingSerializer(listing, data=request.DATA)
#    if serializer.is_valid():
#      serializer.save()
#      return Response(serializer.data)
#    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#  def delete(self, request, product_id, format=None):
#    listing = self.get_object(product_id)
#    listing.delete()
#    return Response(status=status.HTTP_204_NO_CONTENT)



