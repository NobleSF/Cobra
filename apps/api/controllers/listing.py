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

  id = serializers.Field(source='product.id')
  #product = ProductSerializer(many=False, read_only=True)

  #MODEL PROPERTIES
  title = serializers.Field()
  price = serializers.Field(source='display_price')
  shipping_price = serializers.Field(source='display_shipping_price')

  #SERIALIZERS
  materials = serializers.SerializerMethodField('get_materials')
  artisans = serializers.SerializerMethodField('get_artisans')

  def get_materials(self, obj):
    from apps.api.controllers.asset import AssetSerializer
    serializer = AssetSerializer(obj.materials)
    return serializer.data

  def get_artisans(self, obj):
    from apps.api.controllers.asset import AssetSerializer
    serializer = AssetSerializer(obj.product.assets.filter(ilk='artisans'))
    return serializer.data

  class Meta:
    model = Listing
    fields = ('title', 'price', 'shipping_price', 'materials', 'artisans',)


class ListingList(APIView):
  """
  List all listings, or create a new listing.
  """
  def get(self, request, format=None):
    listings = Listing.objects.all()
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data)

  def post(self, request, format=None):
    serializer = ListingSerializer(data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListingDetail(APIView):
  """
  Retrieve, update or delete a listing.
  """
  def get_object(self, product_id):
    try:
      return Listing.objects.get(product_id=product_id)
    except Listing.DoesNotExist:
      raise Http404

  def get(self, request, product_id, format=None):
    listing = self.get_object(product_id)
    serializer = ListingSerializer(listing)
    return Response(serializer.data)

  def put(self, request, product_id, format=None):
    listing = self.get_object(product_id)
    serializer = ListingSerializer(listing, data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, product_id, format=None):
    listing = self.get_object(product_id)
    listing.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


#http://www.django-rest-framework.org/tutorial/3-class-based-views#using-generic-class-based-views
#from rest_framework import generics
#
#class ListingList(generics.ListCreateAPIView):
#    queryset = Listing.objects.all()
#    serializer_class = ListingSerializer
#
#class ListingDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Listing.objects.all()
#    serializer_class = ListingSerializer
