from apps.seller.models.seller import Seller
from rest_framework import serializers
from apps.admin.utils.exception_handling import ExceptionHandler

class SellerSerializer(serializers.ModelSerializer):
  from apps.api.controllers.asset import AssetSerializer

  assets = AssetSerializer(many=False, read_only=True)

  class Meta:
    model = Seller
    fields = ('assets',)
