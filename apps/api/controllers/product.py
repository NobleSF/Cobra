from apps.seller.models.product import Product
from rest_framework import serializers
from apps.admin.utils.exception_handling import ExceptionHandler

class ProductSerializer(serializers.ModelSerializer):
  from apps.api.controllers.asset import AssetSerializer

  assets = AssetSerializer(many=False, read_only=True)

  class Meta:
    model = Product
    fields = ('assets',)
